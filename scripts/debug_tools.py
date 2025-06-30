import numpy as np
import cv2
from scripts.global_variables import state

fps_info = []
fps_info_size = 300


def show_framerate(frame, fps):
    fps_info.append(fps)
    if len(fps_info) == fps_info_size + 1:
        fps_info.pop(0)
    data = np.array(fps_info)
    sorted_data = np.sort(data)
    count = max(1, int(len(data)*0.01))
    lows_percent = np.mean(sorted_data[:count])
    cv2.putText(frame, f"FPS: {fps:.2f}AVE: {np.average(fps_info):.2f}LOWS: {lows_percent:.2f}", (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 2)
        

def show_clicking(frame):
     cv2.putText(frame, f"Clicking: {state['is_clicking']}", (30, 180), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 2)

def draw_border(frame):
    tl = (int(state['calibration_points'][0][0]*state['cap_w']), int(state['calibration_points'][0][1]*state['cap_h']))
    tr = (int(state['calibration_points'][1][0]*state['cap_w']), int(state['calibration_points'][0][1]*state['cap_h']))
    bl = (int(state['calibration_points'][0][0]*state['cap_w']), int(state['calibration_points'][1][1]*state['cap_h']))
    br = (int(state['calibration_points'][1][0]*state['cap_w']), int(state['calibration_points'][1][1]*state['cap_h']))
    cv2.line(frame, tl, tr, (0, 0, 0), 3)
    cv2.line(frame, tl, bl, (0, 0, 0), 3)
    cv2.line(frame, tr, br, (0, 0, 0), 3)
    cv2.line(frame, br, bl, (0, 0, 0), 3)