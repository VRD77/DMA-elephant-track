import cv2
import config

class CameraCapture:
    """
    MODULE 1: Handles opening webcam, capturing frames, resizing,
    and mirroring to match the required architecture.
    """
    def __init__(self):
        # Open webcam via cv2.VideoCapture(0)
        self.cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not self.cap.isOpened():
            raise RuntimeError("Error: Camera not found or cannot be opened. Please check your webcam connection.")
        
        # We handle resizing in the read() method to ensure every frame matches 640x640.
        # But we could also try setting the camera property requests if the hardware supports it.
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        # self.cap.set(cv2.CAP_PROP_FPS, config.FPS_TARGET)
        
    def read(self):
        """
        Reads a frame from the webcam, resizes it, and mirrors it.
        """
        success, frame = self.cap.read()
        if not success:
            return False, None
            
        # Resize to 640x640 for YOLO input
        frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))
        
        # Mirror frame horizontally (selfie view)
        frame = cv2.flip(frame, 1)
        
        return True, frame

    def release(self):
        """Releases the camera resource cleanly."""
        if self.cap.isOpened():
            self.cap.release()
