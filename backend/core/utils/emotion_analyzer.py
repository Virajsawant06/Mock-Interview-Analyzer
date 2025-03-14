import cv2
from deepface import DeepFace
import numpy as np

class FacialExpressionAnalyzer:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    def analyze_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]
            try:
                prediction = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
                return prediction[0]['dominant_emotion']
            except Exception as e:
                print("DeepFace Error:", e)
                return "Unknown"

        return "No Face Detected"
