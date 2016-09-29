import comm_nonblock


def recv(event_loop, sock, f):
    """Read from 'sock' until there's no more data to read.  When finished
       call f(data)."""
    data_list = []

    def read():
        data_part = comm_nonblock.recv(sock)

        if data_part is None:
            f(''.join(data_list))
        else:
            data_list.append(data_part)
            event_loop.on_read_ready(sock, read)

    read()


def send(event_loop, sock, data, f):
    """Send data until there's no more data to send. When finished
       call f(data)."""

    unsent_data = comm_nonblock.send(sock, data)

    if unsent_data is None:
        f()
    else:
        event_loop.on_write_ready(
            sock, lambda: send(event_loop, sock, unsent_data, f)
        )


def send_recv(event_loop, sock, req, f):
    send(event_loop, sock, req, lambda: receive_data())

    def receive_data():
        recv(event_loop, sock, lambda resp: f(resp))
