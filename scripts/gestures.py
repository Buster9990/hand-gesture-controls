import numpy as np
import cv2
import scripts.hands as hands
from scripts.global_variables import state
import time
import datetime
import json

def is_gesture(raised, expected, exact, lower_okay):
    for i in range(len(raised)):
        if exact[i] and raised[i] != expected[i]:
            return False
        if not exact[i] and lower_okay[i] and raised[i] > expected[i]:
            return False
        if not exact[i] and not lower_okay[i] and raised[i] < expected[i]:
            return False
    return True

def get_raised_fingers(hand):
    is_higher_dist = 0.02

    wrist = hand.landmark[0]
    thumb = hand.landmark[4]
    index = hand.landmark[8]
    middle = hand.landmark[12]
    ring = hand.landmark[16]
    pinky = hand.landmark[20]
    tips = [index, middle, ring, pinky]

    raised_arr = []
    for i, t in enumerate(tips):
        # raised if it is higher
        index = 5 + (i*4)
        raised = 3
        for j in range(index+1, index+4):
            point = hand.landmark[j]
            prev = hand.landmark[j-1]
            if prev.y - point.y < is_higher_dist:
                raised -= 1
        raised_arr.append(raised)
    return raised_arr

def compare_gesture(hand, gesture, normalized=True):
    if not normalized:
        gesture = normalize_gesture(gesture)
    total_distance = 0
    for i in range(21):
        hand_l = hand.landmark[i]
        g_l = gesture[i]
        hand_n = (hand_l.x - hand.landmark[0].x, hand_l.y - hand.landmark[0].y, hand_l.z - hand.landmark[0].z)
        distance = pow(hand_n[0] - g_l[0], 2) + pow(hand_n[1] - g_l[1], 2) + pow(hand_n[2] - g_l[2], 2)
        total_distance += np.sqrt(distance)
    return total_distance

def normalize_gesture(gesture):
    g = []
    for landmark in gesture:
        g.append((landmark.x - gesture[0].x, landmark.y - gesture[0].y, landmark.z - gesture[0].z))
    return g

def show_gesture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, state['cap_w'])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, state['cap_h'])
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            return True

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        left_hand, right_hand = hands.process(rgb)
        key = cv2.waitKey(1)
        if key == 32:
            exit()
        elif key == ord('q'):
            save_gesture(left_hand)
        hands.mp_drawing.draw_landmarks(frame, left_hand, hands.mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Gesture saver", frame)

def save_gesture(hand):
    g = []
    for n in hand.landmark:
        g.append((n.x, n.y, n.z))
    file_name = f"{time.time()}.json"
    file = open("gestures/"+file_name, "w")
    json.dump(g, file)
    file.close()

if __name__ == "__main__":
    show_gesture()