import os
import cv2
import easyocr
import matplotlib.pyplot as plt
from itertools import count
from snackbar import alert_window

reader = easyocr.Reader(["en"])
zone_dict = dict()
i = count(start=1)


def process_img(saved_photos):
    for saved_photo in saved_photos:
        path = os.path.join("./", saved_photo)
        print(path)
        zona_img = cv2.imread(path)
        gray_img = cv2.cvtColor(zona_img, cv2.COLOR_BGRA2GRAY)
        read_text(gray_img)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated_img = cv2.dilate(gray_img, kernel, iterations=1)
        read_text(dilated_img)
    clean_text()


def read_text(image):
    results = reader.readtext(image)
    label = results[0][1]
    conf = round(results[0][2], 2)
    zone_dict[next(i)] = (label, conf)


def clean_text():
    max_val = 0
    max_label = None
    for key, values in zone_dict.items():
        if max_val < values[1]:
            max_val = values[1]
            max_label = values[0]
            cleaned_label = ''.join(char for char in max_label if char.isalnum())

    print(f"Label: {cleaned_label} max_value: {max_val}")
    alert_window("Aptiktas vidutinio greičio matuoklis!", cleaned_label)


# process_img(["zone_cropped_1.jpg", "zone_cropped_2.jpg", "zone_cropped_3.jpg"])
# zone_label = clean_text()
# print(zone_dict)
# print(f"Zona nustatyta: {zone_label}")

