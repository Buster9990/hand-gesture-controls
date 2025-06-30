import mediapipe as mp

# MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7,  model_complexity=0)
mp_drawing = mp.solutions.drawing_utils

def process(frame):
    results = hands.process(frame)
    left_hand = None
    right_hand = None
    if results.multi_hand_landmarks:
        handedness_info = results.multi_handedness
        hands_list = results.multi_hand_landmarks
        for idx, hand_info in enumerate(handedness_info):
            label = hand_info.classification[0].label  # "Left" or "Right"
            hand_landmarks = hands_list[idx]

            if label == "Right":
                right_hand = hand_landmarks
            elif label == "Left":
                left_hand = hand_landmarks
                mp_drawing.draw_landmarks(frame, left_hand, mp_hands.HAND_CONNECTIONS)
    return left_hand, right_hand