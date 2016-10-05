import comm
import comm_nonblock
import gen
import json
import sys


def print_password(page_name, resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password for {}: {}".format(page_name, resp['ok'])


def dumper(page_name):
    sock = comm_nonblock.connect(comm.PASSWORD_SERVER)
    password_resp = []

    data = json.dumps(dict(page=page_name))

    # send all data
    while True:
        yield sock, "send"
        data = comm_nonblock.send(sock, data)

        if data is None:
            break

    # receive all data
    while True:
        yield sock, "receive"
        data = comm_nonblock.recv(sock)

        if data is None:
            break

        password_resp.append(data)

    print_password(page_name, password_resp)


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        sys.stderr.write("Expecting one or more arguments, got None.")
        sys.exit(1)

    event_loop = gen.EventLoop()

    page_names = [arg for arg in args]

    gens = [dumper(page) for page in page_names]

    event_loop.run(gens)


if __name__ == '__main__':
    main()
