import select


class EventLoop(object):

    def __init__(self):
        self.readables = {}
        self.writeables = {}

    def step(self, gen):
        try:
            sock, signal = gen.next()
            if signal == "send":
                assert sock not in self.writeables, "sock already used"
                self.writeables[sock] = gen
            elif signal == "receive":
                assert sock not in self.readables, "sock already used"
                self.readables[sock] = gen
            else:
                raise Exception("Unknown signal {}".format(signal))
        except StopIteration:
            return

    def run(self, gen_list):
        for gen in gen_list:
            self.step(gen)

        while self.readables or self.writeables:
            rlist, wlist, xlist = select.select(
                self.readables.keys(), self.writeables.keys(), ()
            )
            assert len(xlist) == 0, "Got exception on socket."

            for sock in rlist:
                gen = self.readables.pop(sock)
                self.step(gen)

            for sock in wlist:
                gen = self.writeables.pop(sock)
                self.step(gen)
