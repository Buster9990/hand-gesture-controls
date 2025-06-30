import cv2
import time
from threading import Thread
import mouse_mover
import debug_tools
import offhand
import hands

from global_variables import state
# Time info
t1 = 100 
t2 = 1

# Webcam

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, state['cap_w'])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, state['cap_h'])

print("Calibration starting. Please point your index finger to each corner of the screen when prompted...")
mouse_move_thread = Thread(target=mouse_mover.move_mouse, daemon=True)
mouse_move_thread.start()



def task():
    global t1, t2
    ret, frame = cap.read()
    if not ret:
        return True

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    left_hand, right_hand = hands.process(rgb)
    if not state['calibrated']:    
        text = f"Point at: {state['corner_names'][len(state['calibration_points'])]}"
        cv2.putText(frame, text, (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)

    offhand.process_offhand(left_hand)
    if right_hand:
        hand = right_hand
        index_tip = hand.landmark[8]


        cam_x, cam_y = index_tip.x, index_tip.y
        if len(state['calibration_points']) == 1:
            pt1 = (int(state['calibration_points'][0][0]*state['cap_w']), int(state['calibration_points'][0][1]*state['cap_h']))
            pt2 = (int(cam_x*state['cap_w']), int(cam_y*state['cap_h']))

            cv2.line(frame, pt1, pt2, (0, 0, 0), 3)
        # Draw finger
        cv2.circle(frame, (int(cam_x * state['cap_w']), int(cam_y * state['cap_h'])), 10, (0, 255, 0), -1)

        if not state['calibrated']:
            # Wait for spacebar press to collect this calibration point1
            key = cv2.waitKey(1)
            if key == 32:  # Spacebar
                state['calibration_points'].append((cam_x, cam_y))
                print(f"Captured point {len(state['calibration_points'])}: {cam_x:.3f}, {cam_y:.3f}")
                if len(state['calibration_points']) == 2:
                    state['calibrated'] = True
                    print("✅ Calibration complete. Start pointing to move the mouse.")
        else:
            cam_x, cam_y = index_tip.x, index_tip.y
            mouse_mover.drag_border((cam_x, cam_y))
            debug_tools.draw_border(frame)

            mouse_mover.handle_mouse_movement(cam_x, cam_y)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        return True
    
    # debugging
    t2 = time.time()
    frames_per_second = 1.0 / (t2-t1)
    t1 = time.time()
    debug_tools.show_framerate(frame, frames_per_second)
    debug_tools.show_clicking(frame)
    
    #img showing
    cv2.imshow("Calibrated Finger Mouse", frame)
    return False



min_sleep_length = 0.005
next_time = time.perf_counter()
while cap.isOpened():
    now = time.perf_counter()
    if now >= next_time:
        # task at hand
        should_end = task()
        if should_end:
            break
        # end of task
        next_time += state['interval']
    sleep_duration = next_time - time.perf_counter()
    if sleep_duration > min_sleep_length:
        time.sleep(sleep_duration)
    else:
        next_time = time.perf_counter()

cap.release()
cv2.destroyAllWindows()