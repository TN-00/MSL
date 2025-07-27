import cv2
import mediapipe as mp

def detect_hand_gesture(image):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True)
    mp_draw = mp.solutions.drawing_utils

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = hands.process(image_rgb)

    gesture = "No hand detected"
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = "Hand detected"  # Placeholder for actual gesture logic

    return gesture
