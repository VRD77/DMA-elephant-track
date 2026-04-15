import cv2
from camera_capture import CameraCapture
from yolo_detector import ElephantCrossingDetector
from alert_engine import AlertEngine
from display_renderer import DisplayRenderer

def main():
    print("Initializing ElephantGuard Custom YOLOv8 Detector Demo...")
    
    try:
        camera = CameraCapture()
    except RuntimeError as e:
        print(f"Failed to start camera: {e}")
        return
        
    detector = ElephantCrossingDetector()
    alert_engine = AlertEngine()
    renderer = DisplayRenderer()
    
    frame_count = 0
    last_detections = []
    
    print("System initialized. Press 'q' to quit cleanly.")
    
    while True:
        success, frame = camera.read()
        if not success:
            print("Failed to capture frame from webcam. Exiting...")
            break
            
        frame_count += 1
        
        # Frame skip: run YOLO on 1 of every 3 frames
        if frame_count % 3 == 0:
            last_detections = detector.detect(frame)
            
        # Crossing state updated every frame using cached detections
        crossing_state = detector.update_crossing_state(last_detections)
        
        # Alert fires BEFORE rendering (low latency)
        if crossing_state["is_crossing"]:
            triggered = alert_engine.trigger(crossing_state, frame_count)
            if triggered:
                renderer.trigger_flash()
                
        # Render last
        renderer.render(frame, crossing_state, alert_engine.alert_count, alert_engine.last_alert_time)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Quit signal received.")
            break

    print("Cleaning up resources...")
    camera.release()
    cv2.destroyAllWindows()
    print("ElephantGuard terminated cleanly.")

if __name__ == "__main__":
    main()
