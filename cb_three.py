import comm
import comm_nonblock
import ev

event_loop = ev.EventLoop()


def connect():
    print "Connecting..."
    sock = comm_nonblock.connect(comm.HELLO_SERVER)
    event_loop.on_read_ready(sock, lambda: read1(sock))


def read1(sock):
    data1 = comm_nonblock.recv(sock)
    print "Got data1: {!r}".format(data1)
    event_loop.on_read_ready(sock, lambda: read2(sock, data1))


def read2(sock, data1):
    data2 = comm_nonblock.recv(sock)
    print "Got data2: {!r}".format(data2)
    event_loop.on_read_ready(sock, lambda: read3(sock, data1, data2))


def read3(sock, data1, data2):
    data3 = comm_nonblock.recv(sock)
    print "Got data3: {!r}".format(data3)
    print "DONE: {!r}".format((data1, data2, data3))

# Start the first fragment.
connect()

print "EventLoop starting..."
event_loop.run()
print "EventLoop finished."
