import cv2
import socket
import pickle

buffer_size = 1000000
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, buffer_size)
HOST = "192.168.1.178"
# HOST = "34.118.39.46"
PORT = 9090
server_address = (HOST, PORT)

cap = cv2.VideoCapture(0)


def ping_server():
    try:
        test_msg = b"ping"
        client_socket.sendto(test_msg, server_address)
        client_socket.settimeout(3)
        try:
            response, _ = client_socket.recvfrom(buffer_size)
            return response == test_msg
        except socket.timeout as t:
            print(t)
            return False
    except Exception as e:
        print(e)
        return False


def frames(i):
    while cap.isOpened():
        print(f"i: {i}")
        if i == 1:
            ok, frame = cap.read()
            if not ok:
                print("Frames not capturing")
            else:
                # Resizing, compressing and to bytes then sending to server
                resized_frame = cv2.resize(frame, (640, 640))
                result, frame_compress = cv2.imencode('.jpg', resized_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                bytes = pickle.dumps(frame_compress)
                client_socket.sendto(bytes, server_address)
                # cv2.imshow("Transmitting video", frame)
                # Getting back the augmented frames
                packet = client_socket.recvfrom(buffer_size)
                data = packet[0]
                # print(f"Getting data {packet}")
                data = pickle.loads(data)
                frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
                print(f"Getting frames back: {frame}")
                return frame
        else:
            client_socket.close()
            cap.release()
