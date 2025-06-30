from threading import Lock
import time
import ctypes
from global_variables import state
import pyautogui
import numpy as np

smooth_steps = 3
wait_time = state['interval'] / smooth_steps



mouse_lock = Lock()
mouse_future_moves = []

def drag_border(index):
    # x-axis
    if index[0] <= 0 or index[0] >= 1 or index[1] <= 0 or index[1] >= 1:
        return
    minx = state['calibration_points'][0][0]
    miny = state['calibration_points'][1][1]
    maxx = state['calibration_points'][1][0]
    maxy = state['calibration_points'][0][1]
    if index[0] < minx:
        if abs(index[0] - minx) > 0.025:
            offset = minx - index[0]
            state['calibration_points'][0] = (minx-offset, maxy)
            state['calibration_points'][1] = (maxx - offset, miny)
    if index[0] > maxx:
        if abs(index[0] - maxx) > 0.025:
            offset =  index[0] - maxx
            state['calibration_points'][0] = (minx+offset, maxy)
            state['calibration_points'][1] = (maxx+offset, miny)
    if index[1] > miny:
        if abs(index[1] - miny) > 0.025:
            offset = miny - index[1]
            state['calibration_points'][0] = (minx, maxy-offset)
            state['calibration_points'][1] = (maxx, miny-offset)
    if index[1] < maxy:
        if abs(index[1] - maxy) > 0.025:
            offset = index[1] - maxy         
            state['calibration_points'][0] = (minx, maxy+offset)
            state['calibration_points'][1] = (maxx, miny+offset)

def move_mouse():
    global mouse_future_moves
    c = 0
    while True:                                                  
        if not mouse_future_moves:
            time.sleep(0.001)
            continue
        if c < len(mouse_future_moves) and c > 0:
            print("Updated!", c) 
        with mouse_lock:
            x, y, t = mouse_future_moves[0]
 
        now = time.time()                    
        delay = t - now
        if delay > 0:
            time.sleep(delay)
        ctypes.windll.user32.SetCursorPos(x, y)
        with mouse_lock:
            mouse_future_moves.pop(0)
            c = len(mouse_future_moves)

def interpolate_position(cam_x, cam_y, ref_points):
    # Extract corners
    tl,  br = ref_points  # each is (x, y) in camera space

    max_y = br[1]
    max_x = br[0]
    min_y = tl[1]
    min_x = tl[0]
    alpha_x = (cam_x - min_x)/(max_x-min_x)
    alpha_y = (cam_y - min_y)/(max_y-min_y)
    screen_x = alpha_x * state['screen_w']
    screen_y = alpha_y * state['screen_h']
    screen_x = min(max(0, screen_x), state['screen_w'])
    screen_y = min(max(0, screen_y), state['screen_h'])

    return int(screen_x), int(screen_y)

def smooth_positions(start_x, start_y, end_x, end_y, steps=3, duration=0.1):
    now = time.time()
    interval = duration / steps
    positions = []
    delta_x = end_x - start_x
    delta_y = end_y - start_y
    step_x = int(delta_x / steps)
    step_y = int(delta_y / steps)
    positions.append((start_x+step_x, start_y+step_y, now))
    for i in range(1, steps):
        t = now + i * interval
        positions.append((positions[i-1][0]+step_x, positions[i-1][1]+step_y, t))
    positions.append((end_x, end_y, now + steps*interval))
    print(positions)
    return positions

def handle_mouse_movement(cam_x, cam_y):
    global mouse_future_moves, smooth_steps
    screen_x, screen_y = interpolate_position(cam_x, cam_y, state['calibration_points'])
    current = pyautogui.position()
    if np.linalg.norm(np.array((screen_x,  screen_y)) - np.array((current.x,current.y))) > state['move_sensitivity']:
        with mouse_lock:
            # mouse_future_moves = smooth_positions(current.x, current.y, screen_x, screen_y, smooth_steps, state['interval'])
            mouse_future_moves.append((screen_x, screen_y, time.time()))