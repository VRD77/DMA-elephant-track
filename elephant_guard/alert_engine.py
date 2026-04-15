import time
import os
import csv
import platform
import subprocess
import threading
from plyer import notification
import config

class AlertEngine:
    """
    MODULE 4: AlertEngine
    Manages notifications, logging, and audio alerts.
    """
    def __init__(self):
        self.last_alert_time = 0
        self.log_file = "alerts_log.csv"
        self.alert_count = 0
        
        # Create CSV if it doesn't exist and write header
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "direction", "delta_x", "delta_y", "yolo_confidence", "frame_number"])

    def trigger(self, crossing_state, frame_number):
        """
        Attempts to trigger an alert if cooldown has passed.
        Returns True if an alert just triggered, False otherwise.
        """
        current_time = time.time()
        
        # Cooldown check
        if current_time - self.last_alert_time < config.ALERT_COOLDOWN_SEC:
            return False
            
        self.last_alert_time = current_time
        self.alert_count += 1
        
        # a) Send desktop push notification via plyer
        try:
            threading.Thread(
                target=notification.notify,
                kwargs=dict(
                    title=config.ALERT_TITLE,
                    message=config.ALERT_MESSAGE,
                    app_name="ElephantGuard v1.0",
                    timeout=5
                ),
                daemon=True
            ).start()
        except Exception as e:
            print(f"Notification failed (plyer issue on some distros): {e}")

        # c) Log event to alerts_log.csv
        direction = crossing_state["direction"] if crossing_state["direction"] else "Unknown"
        best_conf = crossing_state["conf"]
            
        timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp_str, direction, crossing_state["delta_x"], 
                             crossing_state["delta_y"], best_conf, frame_number])
                             
        # d) Play a short system beep across Windows/Mac/Linux
        self._play_beep()
        
        return True
        
    def _play_beep(self):
        """Cross-platform audio alert."""
        system = platform.system()
        try:
            if system == "Windows":
                import winsound
                # Frequency 1000Hz, Duration 500ms
                winsound.Beep(1000, 500)
            elif system == "Darwin": # Mac
                os.system("afplay /System/Library/Sounds/Ping.aiff &")
            else: # Linux
                # We try some common commands, or a simple print ASCII bell
                os.system("echo -e '\a'")
                # if sox is available
                # subprocess.run(["play", "-n", "synth", "0.5", "sine", "1000"], stderr=subprocess.DEVNULL)
        except Exception as e:
            print(f"Beep audio failed: {e}")
