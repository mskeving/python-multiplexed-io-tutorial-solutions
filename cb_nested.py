import comm
import comm_nonblock
import ev

event_loop = ev.EventLoop()


def get_data():
    def read1():
        data1 = comm_nonblock.recv(sock)
        print "Got data1: {!r}".format(data1)

        def read2():
            data2 = comm_nonblock.recv(sock)
            print "Got data2: {!r}".format(data2)

            def read3():
                data3 = comm_nonblock.recv(sock)
                print "Got data3: {!r}".format(data3)
                print "DONE: {!r}".format((data1, data2, data3))

            event_loop.on_read_ready(sock, read3)

        event_loop.on_read_ready(sock, read2)

    print "Connecting..."
    sock = comm_nonblock.connect(comm.HELLO_SERVER)

    event_loop.on_read_ready(sock, read1)


# Start the first fragment.
get_data()

print "EventLoop starting..."
event_loop.run()
print "EventLoop finished."
