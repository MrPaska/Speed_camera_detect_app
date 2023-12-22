import cv2
import matplotlib.pyplot as plt
import easyocr


def read_zone():
    zona_img = cv2.imread("zone_cropped.jpg")
    gray_img = cv2.cvtColor(zona_img, cv2.COLOR_BGRA2GRAY)

    reader = easyocr.Reader(["en"])
    result = reader.readtext(gray_img)
    text = result[0][1]
    cleaning = ''.join(char for char in text if char.isalnum())
    print(cleaning)
    return cleaning
