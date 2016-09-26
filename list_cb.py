import json
import sys

import comm_nonblock
import ev

from comm import PASSWORD_SERVER
from comm_ev import send, recv

event_loop = ev.EventLoop()


def print_password(page_name, resp):
    print "print page name: {}".format(page_name)
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password for {}: {}".format(page_name, resp['ok'])


def send_data(sock, req, page):
    # closure to keep page name
    send(event_loop, sock, req, lambda sock: receive_data(sock, page))


def receive_data(sock, page_name):
    recv(event_loop, sock, lambda resp: print_password(page_name, resp))


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        sys.stderr.write("Expecting one or more arguments, got None.")
        sys.exit(1)

    page_names = [arg for arg in args]

    for page in page_names:
        sock = comm_nonblock.connect(PASSWORD_SERVER)
        req = json.dumps(dict(page=page))

        send_data(sock, req, page)


if __name__ == '__main__':
    main()

    print "EventLoop starting..."
    event_loop.run()
    print "EventLoop finished."
