import cv2
import socket
import pickle
import numpy as np

buffer_size = 1000000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)
HOST = "192.168.1.112"
PORT = 9090
client_address = (HOST, PORT)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ok, frame = cap.read()
    if not ok:
        print("Frames not capturing")
    else:
        # Resizing, compressing and to bytes then sending to server
        resized_frame = cv2.resize(frame, (640, 640))
        result, frame_compress = cv2.imencode('.jpg', resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        bytes = pickle.dumps(frame_compress)
        client_socket.sendto(bytes, client_address)
        # cv2.imshow("Transmitting video", frame)
        # Getting back the augmented frames
        packet = client_socket.recvfrom(buffer_size)
        data = packet[0]
        print(f"Getting data {data}")
        data = pickle.loads(data)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        print(img)
        #cv2.imshow("Augmented video", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Shutting down!")
            client_socket.close()
            break