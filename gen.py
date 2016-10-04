import select


class EventLoop(object):

    def __init__(self):
        self.socks_to_gens = {}

    def next(self, gen):
        try:
            sock = gen.next()
            assert self.socks_to_gens.get(sock) is None, "sock already used"
            self.socks_to_gens[sock] = gen
        except StopIteration:
            return

    def run(self, *args):
        for gen in args:
            self.next(gen)

        while self.socks_to_gens:
            rlist, _, _ = select.select(self.socks_to_gens.keys(), (), ())

            for sock in rlist:
                gen = self.socks_to_gens.pop(sock)
                self.next(gen)
