import comm_nonblock


def recv(event_loop, sock, f):
    """Read from 'sock' until there's no more data to read.  When finished
           call f(data)."""
    all_data = ""

    def read(all_data):
        data = comm_nonblock.recv(sock)

        if data is not None:
            print "Got data piece: {!r}".format(data)
            all_data += data
            event_loop.on_read_ready(sock, lambda: read(all_data))

        else:
            f(all_data)

    event_loop.on_read_ready(sock, lambda: read(all_data))
