import comm_nonblock
import gen


def send_data(sock, data):
    while True:
        yield gen.Write(sock)
        data = comm_nonblock.send(sock, data)
        if data is None:
            break


def receive_data(sock, data):
    password_response = []

    while True:
        yield gen.Read(sock), password_response
        data = comm_nonblock.recv(sock)
        if data is None:
            break

        password_response.append(data)
