import pyautogui

state = {
    "fps":                30,
    "interval":           0,
    "cap_w":              640,
    "cap_h":              480,
    "screen_w":           pyautogui.size()[0],
    "screen_h":           pyautogui.size()[1],
    "calibrated":         False,
    "calibration_points": [],
    "corner_names":       ["TOP-LEFT", "BOTTOM_RIGHT"],
    "move_sensitivity":   5,
    "is_clicking":        False,
    "mouse_move_thread":  None

}
state['interval'] = 1.0 / state['fps']