import asyncio

import cv2 as cv
from ultralytics import YOLO
import threading

from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, Create3

robot = Create3(Bluetooth('bard'))
direction = "none"
# robot_busy = False  # prevent spamming robot.play()

# sliding window of three frames to calc trajectory
def get_trajectory(frames):
    pass

@event(robot.when_play)
async def play(robot):
    # global robot_busy
    global direction
    print("Connected to the robot...")
    await robot.set_lights_rgb(0, 255, 0)
    await robot.play_note(440, 0.25)

    while True:
        print("In move loop...")
        if direction == "left":
            # await robot.move(50)
            await robot.set_wheel_speeds(100, 100)
            direction = "none"
        elif direction == "right":
            # await robot.move(-100)
            await robot.set_wheel_speeds(-100, -100)
            direction = "none"
        else:
            await robot.stop()
        await asyncio.sleep(0.1)  # small delay to prevent spamming commands
        

    # robot_busy = False  # done moving

def move_robot():
    # global robot_busy
    # robot_busy = True
    robot.play()

puck_model = YOLO("runs/detect/train6/weights/best.pt")
DISPLAY_COLOR = (255, 0, 0)


threading.Thread(target=move_robot, daemon=True).start()

cap = cv.VideoCapture(1, cv.CAP_AVFOUNDATION)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame_width = frame.shape[1]
    results = puck_model(frame, verbose=False)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        center_x = (x1 + x2) / 2
        position = "left" if center_x < frame_width / 2 else "right"
        label = f"{puck_model.names[int(box.cls)]} {position}"

        cv.rectangle(frame, (x1, y1), (x2, y2), DISPLAY_COLOR, 4)
        cv.putText(frame, label, (x1, y1 - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 1.2, DISPLAY_COLOR, 4)

        # print('is robot busy?', robot_busy)
        if "puck" in label:  # and not robot_busy:
            print(f"Detected puck at {position}")
            direction = position
        

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()