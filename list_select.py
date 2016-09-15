import json
import select
import sys

import comm
import comm_nonblock


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        sys.stderr.write("Expecting one or more arguments, got None.")
        sys.exit(1)

    page_names = [arg for arg in args]

    sock_to_req = {}
    sock_to_resp = {}

    for page_name in page_names:
        sock = comm_nonblock.connect(comm.PASSWORD_SERVER)
        sock_to_req[sock] = json.dumps(dict(page=page_name))
        sock_to_resp[sock] = []  # to store bytes we receive

    # send all requests
    writeables = sock_to_req.keys()
    while len(writeables) > 0:

        _, wlist, xlist = select.select((), writeables, ())
        assert len(xlist) == 0, "Got exceptions on sockets."

        for sock in wlist:
            req = sock_to_req[sock]
            new_req = comm_nonblock.send(sock, req)

            if new_req is None:
                writeables.remove(sock)
                continue

            sock_to_req[sock] = new_req

    # read all requests
    readables = sock_to_resp.keys()
    while len(readables) > 0:

        rlist, _, xlist = select.select(readables, (), ())
        assert len(xlist) == 0, "Got exceptions on sockets."

        for sock in rlist:
            data_list = sock_to_resp[sock]
            data_part = comm_nonblock.recv(sock)

            if data_part is None:
                handle_response(data_list)
                readables.remove(sock)
                continue
            if len(data_part) > 0:
                data_list.append(data_part)

            sock_to_resp[sock] = data_list


def handle_response(resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password: {}".format(resp['ok'])

if __name__ == '__main__':
    main()
