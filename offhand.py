import ctypes
import gestures
import numpy as np

from global_variables import state

increase_factor = 0.66
last_offhand_pos = None

def process_offhand(offhand):
    global last_offhand_pos
    if offhand == None:
        if state['is_clicking']:
            state['is_clicking'] = False
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) 
        return
    raised = gestures.get_raised_fingers(offhand)


    handle_clicking(raised)

    if last_offhand_pos == None:
        last_offhand_pos = offhand
        return
    
    change_sensitivity = gestures.is_gesture(raised, [3, 3, 1, 1], [True, True, False, False], [False, False, True, True])
    if change_sensitivity and len(state['calibration_points']) == 2: 
        change_rateX = offhand.landmark[5].x - last_offhand_pos.landmark[5].x
        change_rateY = offhand.landmark[5].y - last_offhand_pos.landmark[5].y
        change_rateX *= increase_factor
        change_rateY *= increase_factor
        new_tl = state['calibration_points'][0][0]-change_rateX, state['calibration_points'][0][1]-change_rateY
        new_br = state['calibration_points'][1][0]+change_rateX, state['calibration_points'][1][1]+change_rateY
        state['calibration_points'][0] = new_tl
        state['calibration_points'][1] = new_br

    last_offhand_pos = offhand

def handle_clicking(fingers):
    click_down = gestures.is_gesture(fingers, [3, 0, 0, 0], [True, True, True, True], [False, False, False, False])
    print(fingers, click_down)
    if (not state['is_clicking']) and (click_down):
        state['is_clicking'] = True
        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # Left down
    if state['is_clicking'] and (not click_down):
        state['is_clicking'] = False
        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # Left up
