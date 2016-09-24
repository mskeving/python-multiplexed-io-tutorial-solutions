import comm
import comm_nonblock
import ev

from comm_ev import recv

event_loop = ev.EventLoop()


def print_data(data):
    print "Got all data: {!r}".format(data)


if __name__ == "__main__":
    print "Connecting..."
    sock = comm_nonblock.connect(comm.HELLO_SERVER)

    recv(event_loop, sock, print_data)

    print "EventLoop starting..."
    event_loop.run()
    print "EventLoop finished."
