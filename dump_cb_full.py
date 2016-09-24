import comm
import comm_nonblock
import ev

event_loop = ev.EventLoop()


def get_data():
    def read():
        data = comm_nonblock.recv(sock)
        if data is not None:
            print "Got data: {!r}".format(data)
            event_loop.on_read_ready(sock, read)

    print "Connecting..."
    sock = comm_nonblock.connect(comm.HELLO_SERVER)

    event_loop.on_read_ready(sock, read)


if __name__ == "__main__":
    get_data()

    print "EventLoop starting..."
    event_loop.run()
    print "EventLoop finished."
