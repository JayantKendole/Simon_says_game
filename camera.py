# camera.py
import cv2

class Camera:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)  # Use the first connected camera
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            exit()

    def get_frame(self):
        ret, frame = self.cap.read()
        if ret:
            return frame
        else:
            print("Error: Failed to capture frame.")
            return None

    def release(self):
        self.cap.release()

    def show_frame(self, frame):
        if frame is not None:
            cv2.imshow("Camera Feed", frame)
