import select


class EventLoop(object):

    def __init__(self):
        self.readables = {}
        self.writeables = {}

    def on_read_ready(self, sock, f):
        """When 'sock' is ready to be read, call the function 'f'"""
        assert self.readables.get(sock) is None, "read sock already being used"

        self.readables[sock] = f

    def on_write_ready(self, sock, f):
        """When 'sock' is ready to be written, call the function 'f'"""
        assert self.readables.get(sock) is None, "read sock already being used"

        self.writeables[sock] = f

    def run(self):
        """As long as there are sockets people are waiting on, keep
           looping and processing the callbacks."""
        while self.readables or self.writeables:
            rlist, wlist, _ = select.select(self.readables.keys(),
                                            self.writeables.keys(), ())

            for sock in rlist:
                f = self.readables.pop(sock)
                f()

            for sock in wlist:
                f = self.writeables.pop(sock)
                f()
