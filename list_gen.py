import json
import sys

import comm
import comm_nonblock
import gen

def main():
    args = sys.argv[1:]

    if len(args) == 0:
        sys.stderr.write("You must specify a list of pages on the command line.\n")
        sys.exit(1)

    event_loop = gen.EventLoop()
    event_loop.run(*[get_pw(page_name) for page_name in args])

def get_pw(page_name):
    sock = comm_nonblock.connect(comm.PASSWORD_SERVER)
    req = json.dumps(dict(page=page_name))
    while True:
        yield gen.Write(sock)
        req = comm_nonblock.send(sock, req)
        if req is None:
            break

    data_list = []
    while True:
        yield gen.Read(sock)
        data_part = comm_nonblock.recv(sock)
        if data_part is None:
            break
        data_list.append(data_part)
    data = b''.join(data_list)
    resp = json.loads(data)

    if 'ok' in resp:
        print "{}: {}".format(page_name, resp['ok'])
    else:
        print "ERROR: {!r}".format(resp['error'])


if __name__ == '__main__':
    main()
