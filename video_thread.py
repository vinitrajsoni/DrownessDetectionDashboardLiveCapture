from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import mediapipe as mp
import time
from PyQt5.QtGui import QImage
from utils import eye_aspect_ratio, mouth_aspect_ratio, drowsiness_probability, play_beep
from constants import LEFT_EYE_IDX, RIGHT_EYE_IDX, MOUTH_IDX, ALERT_PROB_RED, ALERT_PROB_YELLOW

class VideoThread(QThread):
    change_pixmap = pyqtSignal(QImage)
    update_data = pyqtSignal(float, float, float)
    alert_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.running = True
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.last_alert_time = 0.0
        self.ALERT_COOLDOWN = 4.0
        
    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.alert_signal.emit("Camera not accessible")
            return
            
        while self.running:
            ret, frame = cap.read()
            if not ret:
                QThread.msleep(10)
                continue
                
            h, w = frame.shape[:2]
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            ear, mar, drows_prob = 0.0, 0.0, 0.0
            
            if results.multi_face_landmarks:
                landmarks = [(int(lm.x * w), int(lm.y * h)) for lm in results.multi_face_landmarks[0].landmark]
                
                # Draw small green dots for each landmark
                for x, y in landmarks:
                    cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)
                
                # EAR calculation
                try:
                    ear = (eye_aspect_ratio(landmarks, LEFT_EYE_IDX) +
                           eye_aspect_ratio(landmarks, RIGHT_EYE_IDX)) / 2
                except:
                    ear = 0.0
                
                # MAR calculation
                try:
                    mar = mouth_aspect_ratio(
                        landmarks,
                        MOUTH_IDX["top"],
                        MOUTH_IDX["bottom"],
                        MOUTH_IDX["left"],
                        MOUTH_IDX["right"]
                    )
                except:
                    mar = 0.0
                
                # Drowsiness probability
                drows_prob = drowsiness_probability(ear, mar)
                
                # Alert logic
                if drows_prob >= ALERT_PROB_RED and (time.time() - self.last_alert_time) > self.ALERT_COOLDOWN:
                    self.alert_signal.emit("red")
                    play_beep()
                    self.last_alert_time = time.time()
                elif drows_prob >= ALERT_PROB_YELLOW:
                    self.alert_signal.emit("yellow")
                else:
                    self.alert_signal.emit("green")
            
            # Emit EAR, MAR, probability for plotting
            self.update_data.emit(ear, mar, drows_prob)
            
            # Convert frame with landmarks to QImage
            qt_image = QImage(frame.data, w, h, w*3, QImage.Format_BGR888)
            self.change_pixmap.emit(qt_image)
            
            QThread.msleep(10)
            
        cap.release()
        
    def stop(self):
        self.running = False
        self.wait()
