import cv2, socket
import pickle
from bounding_boxes2 import recognition
import torch

print(torch.cuda.is_available())

buffer_size = 1000000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)

HOST = "192.168.1.178"
PORT = 9090
server_address = (HOST, PORT)
server_socket.bind(server_address)

while True:
    # Getting frames from client
    packet = server_socket.recvfrom(buffer_size)
    clientip = packet[1][0]
    clientport = packet[1][1]
    print(f"Getting packets from: {clientip}, {clientport}")
    data = packet[0]
    if data == b"ping":
        server_socket.sendto(data, (clientip, clientport))
    else:
        # Converting from bytes to frames for cv2
        data = pickle.loads(data)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)
        # Recognition
        frame = recognition(img)
        # Sending back to client
        # Compressing and to bytes
        result, frame_compress = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
        bytes = pickle.dumps(frame_compress)
        print(f"Sending to: {clientip}, {clientport}")
        server_socket.sendto(bytes, (clientip, clientport))
