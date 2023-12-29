from ultralytics import YOLO
import cvzone
import math
from statistics import post_statistics
from datetime import datetime, timedelta
import play_voice
from snackbar import alert_window
import cv2
from image_processing import process_img
from itertools import count

classes = ["momentinis", "vidutinis", "zona"]
model = YOLO("best2_openvino_model", task='detect')
new_datetime = datetime.now()
i = 0
saved_photos = []
buttons = {
    "momentinis": None,
    "vidutinis": None,
    "zona": None
}


def params(moment, avg, zone):
    buttons["momentinis"] = moment
    buttons["vidutinis"] = avg
    buttons["zona"] = zone


def recognition(frames, user_id):
    global new_datetime, i
    vidutinis = False
    current_datetime = datetime.now()

    if current_datetime >= new_datetime:
        results = model(frames)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                conf = math.ceil(box.conf * 100) / 100
                cls = int(box.cls[0])
                cvzone.cornerRect(frames, (x1, y1, w, h), l=30, t=5, rt=1, colorR=(255, 0, 255), colorC=(0, 255, 0))
                print(box)

                if conf >= 0.8 and classes[cls] == "momentinis":
                    play_voice.play_voice(0)
                    alert_window("Aptiktas momentinis greičio matuoklis!")
                    new_datetime = current_datetime + timedelta(seconds=5)
                if conf >= 0.8 and classes[cls] == "vidutinis":
                    vidutinis = True
                if conf >= 0.8 and classes[cls] == "zona" and vidutinis is True:
                    i += 1
                    print(vidutinis)
                    get_zona_box(frames, x1, x2, y1, y2, i)
                    new_datetime = current_datetime + timedelta(seconds=.5)
                    print(i)
                    if i >= 3:
                        process_img(saved_photos)
                        saved_photos.clear()
                        play_voice.play_voice(1)
                        i = 0
                        new_datetime = current_datetime + timedelta(seconds=2)
                    else:
                        pass
                cvzone.putTextRect(frames, f'{cls} {conf}', (max(0, x1), max(35, y1)), scale=0.7, thickness=1)

        return frames


def get_zona_box(frames, x1, x2, y1, y2, n):
    photo = f"zone_cropped_{n}.jpg"
    zona_box = frames[y1:y2, x1:x2]
    try:
        cv2.imwrite(photo, zona_box)
        saved_photos.append(photo)
        print("foto saved")
    except Exception as e:
        print(f"failed to save photo {e}")

