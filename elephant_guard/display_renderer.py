import cv2
import time
import config

class DisplayRenderer:
    def __init__(self):
        self.window_name = "ElephantGuard - YOLOv8 Demo"
        self.alert_flash_end_time = 0
        self.last_frame_time = time.time()
        
    def trigger_flash(self):
        """Sets the duration for the red full-screen flash to 3 seconds."""
        self.alert_flash_end_time = time.time() + 3.0

    def render(self, frame, crossing_state, alert_count=0, last_alert_time=0):
        h, w, _ = frame.shape
        current_time = time.time()
        
        # 1. Calculate FPS
        fps = 1.0 / (current_time - self.last_frame_time + 1e-9)
        self.last_frame_time = current_time
        
        # 2. Check for Red Flash Alert state
        in_alert_state = current_time < self.alert_flash_end_time
        
        # Draw bounding box for the target elephant if detected
        if crossing_state["elephant_detected"] and crossing_state["bbox"]:
            x1, y1, x2, y2 = crossing_state["bbox"]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            label = f"Elephant  conf: {crossing_state['conf']:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                        
        # Draw Trail
        trajectory = crossing_state.get("trajectory", [])
        for pt in trajectory:
            cv2.circle(frame, pt, 5, (0, 255, 0), -1)
            
        if len(trajectory) > 1:
            pt1 = trajectory[0]
            pt2 = trajectory[-1]
            cv2.arrowedLine(frame, pt1, pt2, (0, 165, 255), 3, tipLength=0.2)

        if in_alert_state:
            # Red full-screen tint flash
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (w, h), (0, 0, 255), -1)
            cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            
            # Draw RED ALERT BANNER
            banner_text = "ELEPHANT CROSSING DETECTED"
            text_size = cv2.getTextSize(banner_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
            text_x = (w - text_size[0]) // 2
            cv2.rectangle(frame, (text_x - 10, h // 2 - 40), (text_x + text_size[0] + 10, h // 2 + 10), (0, 0, 255), -1)
            cv2.putText(frame, banner_text, (text_x, h // 2), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
            
        # 3. HUD (Heads Up Display) top-left panel
        if in_alert_state:
            status = "CROSSING ALERT"
            status_color = (0, 0, 255) # Red
        elif crossing_state["elephant_detected"]:
            status = "ELEPHANT DETECTED"
            status_color = (0, 255, 255) # Yellow
        else:
            status = "SCANNING"
            status_color = (0, 255, 0) # Green
            
        # Background rect for HUD
        cv2.rectangle(frame, (10, 10), (320, 155), (0, 0, 0), -1)
        
        cv2.putText(frame, f"FPS: {int(fps)}", (20, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
        cv2.putText(frame, f"Status: {status}", (20, 55), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)
                    
        direction_str = f" {crossing_state['direction']}" if crossing_state['direction'] else ""
        cv2.putText(frame, f"Delta X (live): {crossing_state['delta_x']:+} px {direction_str}", (20, 80), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
        cv2.putText(frame, f"Confidence: {crossing_state['conf']:.2f}", (20, 105), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
        last_alert_str = "Never"
        if last_alert_time > 0:
            last_alert_str = time.strftime("%H:%M:%S", time.localtime(last_alert_time))
            
        cv2.putText(frame, f"Alerts: {alert_count} | Last: {last_alert_str}", (20, 130), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                    
        # 4. Show the frame
        cv2.imshow(self.window_name, frame)
