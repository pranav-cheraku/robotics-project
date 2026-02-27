import cv2 as cv
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
DISPLAY_COLOR = (255, 0, 0)  # Green color for bounding boxes and text
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    frame_width = frame.shape[1]
    results = model(frame, classes=[32],verbose=False)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        center_x = (x1 + x2) / 2
        position = "left" if center_x < frame_width / 2 else "right"
        label = f"{model.names[int(box.cls)]} {position}"

        cv.rectangle(frame, (x1, y1), (x2, y2), DISPLAY_COLOR, 4)
        cv.putText(frame, label, (x1, y1 - 10),
                   cv.FONT_HERSHEY_SIMPLEX, 1.2, DISPLAY_COLOR, 4)
        
        print(f"{model.names[int(box.cls)]}: {position}")

    cv.imshow('frame', frame)
    if cv.waitKey(1) == ord('q'):
        break

cap.release()
cv.destroyAllWindows()