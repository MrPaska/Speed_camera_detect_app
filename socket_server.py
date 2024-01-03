import cv2, imutils, socket
import pickle
from boundin_boxes2 import recognition

width = 400
buffer_size = 1000000
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)
HOST = "192.168.1.112"
PORT = 9090
server_address = (HOST, PORT)
server_socket.bind(server_address)
labas = b"labas"
while True:
    # Getting frames from client
    packet = server_socket.recvfrom(buffer_size)
    print(f"Packet {packet}")
    clientip = packet[1][0]
    data = packet[0]
    # Converting from bytes to frames for cv2
    data = pickle.loads(data)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    # Recognition
    # frame = recognition(img)
    # Sending back to client
    # Compressing and to bytes
    result, frame_compress = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
    bytes = pickle.dumps(frame_compress)
    # server_socket.sendto(bytes, (clientip, PORT))
    server_socket.sendto(labas, (clientip, PORT))

    # cv2.imshow("Reciving video", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        print("Shutting down!")
        server_socket.close()
        break


