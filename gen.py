import select
import types


class EventLoop(object):

    def __init__(self):
        self.reads = {}
        self.writes = {}
        self.subgen_to_gen = {}

    def run(self, *gens):
        for gen in gens:
            self.step(gen)

        while len(self.reads) > 0 or len(self.writes) > 0:
            rlist = self.reads.keys()
            wlist = self.writes.keys()
            rlist, wlist, xlist = select.select(rlist, wlist, rlist+wlist)
            assert len(xlist) == 0, "Got exception on socket."

            for sock in rlist:
                gen = self.reads.pop(sock)
                self.step(gen)

            for sock in wlist:
                gen = self.writes.pop(sock)
                self.step(gen)

    def step(self, gen, command=None):
        try:
            command = gen.send(command)
        except StopIteration:
            parent_gen = self.subgen_to_gen.pop(gen, None)
            if parent_gen:
                self.step(parent_gen, command)
            return

        if isinstance(command, types.GeneratorType):
            sub_gen = command
            self.step(sub_gen)
            self.subgen_to_gen[sub_gen] = gen
        elif isinstance(command, Read):
            assert command.sock not in self.reads
            self.reads[command.sock] = gen
        elif isinstance(command, Write):
            assert command.sock not in self.writes
            self.writes[command.sock] = gen
        else:
            self.step(gen, command)


class Read(object):
    def __init__(self, sock):
        self.sock = sock


class Write(object):
    def __init__(self, sock):
        self.sock = sock
