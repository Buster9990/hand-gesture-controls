import pyautogui
import tkinter as tk
from tkinter import ttk
import threading

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

sensitivity_max = 50
sensitivity_min = 0
slider_sensitivity: ttk.Scale
label_sensitivity: tk.Label


def sliders_window():
    global slider_sensitivity, label_sensitivity
    root = tk.Tk()
    root.title("Sliders")

    label_sensitivity = tk.Label(root, text="Sensitivity")
    label_sensitivity.pack()
    slider_sensitivity = ttk.Scale(root, from_=sensitivity_min, to=sensitivity_max, value=state['move_sensitivity'], orient="horizontal", command=slider_change)
    slider_sensitivity.pack()
    root.mainloop()

def settings_change():
    thread = threading.Thread(target=sliders_window, daemon=True)
    thread.start()

def slider_change(value):
    global label_sensitivity
    label_sensitivity.config(text="Sensitivity: " + str(int(float(value))))
    label_sensitivity.pack()
    state['move_sensitivity'] = float(value)
    print("move", state['move_sensitivity'])