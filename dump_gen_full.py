import comm
import comm_nonblock
import gen


def main():
    event_loop = gen.EventLoop()
    event_loop.run(dumper())


def dumper():
    sock = comm_nonblock.connect(comm.HELLO_SERVER)

    while True:
        yield sock
        data = comm_nonblock.recv(sock)

        if data is None:
            break

        print "Got data: {!r}".format(data)


if __name__ == '__main__':
    main()
