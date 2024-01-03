from ultralytics import YOLO
import cv2, cvzone, math
from datetime import datetime, timedelta

classes = ["momentinis", "vidutinis", "zona"]
model = YOLO("best2_openvino_model", task='detect')


def recognition(frames):
    results = model(frames)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2-x1, y2-y1
            conf = math.ceil(box.conf * 100) / 100
            cls = int(box.cls[0])
            cvzone.cornerRect(frames, (x1, y1, w, h), l=30, t=5, rt=1, colorR=(255, 0, 255), colorC=(0, 255, 0))
            cvzone.putTextRect(frames, f'{cls} {conf}', (max(0, x1), max(35, y1)), scale=0.7, thickness=1)
    return frames

