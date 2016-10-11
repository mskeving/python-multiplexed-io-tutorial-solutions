import comm_nonblock
import gen


def send(sock, data):
    while True:
        yield gen.Write(sock)
        data = comm_nonblock.send(sock, data)
        if data is None:
            break


def recv(sock):
    data_list = []
    while True:
        yield gen.Read(sock)
        data_part = comm_nonblock.recv(sock)

        if data_part is None:
            data = b''.join(data_list)
            yield data
            break

        data_list.append(data_part)
