from ultralytics import YOLO

# Load a COCO-pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Display model information (optional)
model.info()

# Load data


# Train the model on the COCO8 example dataset for 100 epochs
results = model.train(data="puckDataset/data.yaml", 
                      epochs=50, imgsz=640, batch=16)




# save model