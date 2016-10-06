import comm_nonblock


def send_data(sock, data):
    while True:
        yield sock, "send"
        data = comm_nonblock.send(sock, data)

        if data is None:
            break


def receive_data(sock, data):
    password_response = []
    while True:
        yield sock, "receive", password_response
        data = comm_nonblock.recv(sock)

        if data is None:
            break

        password_response.append(data)
