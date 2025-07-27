import cv2, numpy as np
from channels.generic.websocket import AsyncWebsocketConsumer
import mediapipe as mp

# to detect the face from the webcam and 

mp_holistic = mp.solutions.holistic
mp_draw = mp.solutions.drawing_utils

class DetectConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.holistic = mp_holistic.Holistic(min_detection_confidence=0.5,
                                             min_tracking_confidence=0.5)

    async def disconnect(self, close_code):
        self.holistic.close()

    async def receive(self, bytes_data=None, text_data=None):
        arr = np.frombuffer(bytes_data, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.holistic.process(img)
        height, width, _ = frame.shape
        boxes = []
        if results.face_landmarks:
            xs = [lm.x for lm in results.face_landmarks.landmark]
            ys = [lm.y for lm in results.face_landmarks.landmark]
            boxes.append({
                'type': 'face',
                'box': [
                    int(min(xs)*width), int(min(ys)*height),
                    int(max(xs)*width), int(max(ys)*height),
                ],
            })
        if results.pose_landmarks:
            ys = [lm.y for i, lm in enumerate(results.pose_landmarks.landmark) if lm.visibility > .5 and i in range(0,24)]
            if ys:
                y_min = min(ys)*height
                boxes.append({
                    'type': 'upper_body',
                    'box': [0, int(y_min), width, height], 
                })
        await self.send_json({'boxes': boxes})
