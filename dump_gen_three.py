import comm
import comm_nonblock
import gen


def main():
    event_loop = gen.EventLoop()
    event_loop.run(dumper())


def dumper():
    sock = comm_nonblock.connect(comm.HELLO_SERVER)

    yield sock  # "resume me when there's data to recv on sock"
    data1 = comm_nonblock.recv(sock)
    print "Got data1: {!r}".format(data1)

    yield sock
    data2 = comm_nonblock.recv(sock)
    print "Got data2: {!r}".format(data2)

    yield sock
    data3 = comm_nonblock.recv(sock)
    print "Got data3: {!r}".format(data3)

if __name__ == '__main__':
    main()
