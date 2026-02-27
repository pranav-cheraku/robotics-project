import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    results = model(frame, verbose=False)

    annotated_frame = results[0].plot()

    cv.imshow('frame', annotated_frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()