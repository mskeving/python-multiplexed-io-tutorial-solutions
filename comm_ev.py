import comm_nonblock


def recv(event_loop, sock, f):
    """Read from 'sock' until there's no more data to read.  When finished
       call f(data)."""
    all_data = ""

    def read(all_data):
        data = comm_nonblock.recv(sock)

        if data is not None:
            all_data += data
            event_loop.on_read_ready(sock, lambda: read(all_data))

        else:
            f(all_data)

    event_loop.on_read_ready(sock, lambda: read(all_data))


def send(event_loop, sock, data, f):
    """Send data until there's no more data to send. When finished
       call f(data)."""

    def send_data(all_data):
        unsent_data = comm_nonblock.send(sock, all_data)

        if unsent_data is not None:
            event_loop.on_write_ready(sock, lambda: send_data(unsent_data))

        else:
            f(sock)

    event_loop.on_write_ready(sock, lambda: send_data(data))
