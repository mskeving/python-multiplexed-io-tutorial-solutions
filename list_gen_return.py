import json
import sys

import comm
import comm_nonblock
import gen
from list_gen_send_helper import send, recv


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

    yield send(sock, req)

    data = yield recv(sock)

    resp = json.loads(data)
    if 'ok' in resp:
        print "{}: {}".format(page_name, resp['ok'])
    else:
        print "ERROR: {!r}".format(resp['error'])


if __name__ == '__main__':
    main()
