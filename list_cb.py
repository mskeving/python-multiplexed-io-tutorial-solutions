import json
import sys

import comm_nonblock
import ev

from comm import PASSWORD_SERVER
from comm_ev import send, recv


def print_password(page_name, resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password for {}: {}".format(page_name, resp['ok'])


def start(event_loop, page_name):
    sock = comm_nonblock.connect(PASSWORD_SERVER)
    req = json.dumps(dict(page=page_name))
    send(event_loop, sock, req, lambda: receive_data())

    def receive_data():
        recv(event_loop, sock, lambda resp: handle_response(resp))

        def handle_response(resp):
            print_password(page_name, resp)


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        sys.stderr.write("Expecting one or more arguments, got None.")
        sys.exit(1)

    event_loop = ev.EventLoop()

    page_names = [arg for arg in args]

    for page_name in page_names:
        start(event_loop, page_name)

    event_loop.run()


if __name__ == '__main__':
    main()
