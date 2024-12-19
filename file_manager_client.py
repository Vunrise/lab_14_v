import socket

HOST = "localhost"
PORT = 9090


def start_client():
    while True:
        sock = socket.socket()
        sock.connect((HOST, PORT))

        request = input("myftp@shell$ ")
        sock.send(request.encode())

        response = sock.recv(1024).decode()
        print(response)

        sock.close()

        if request.startswith("exit"):
            break


if __name__ == "__main__":
    start_client()
