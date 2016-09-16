import json
import select
import sys

import comm
import comm_nonblock


class SocketInfo():
    def __init__(self, page_name, req, resp):
        self.page_name = page_name
        self.req = req
        self.resp = resp


def main():
    args = sys.argv[1:]

    if len(args) < 1:
        sys.stderr.write("Expecting one or more arguments, got None.")
        sys.exit(1)

    page_names = [arg for arg in args]

    sock_to_info = {}

    for page_name in page_names:
        sock = comm_nonblock.connect(comm.PASSWORD_SERVER)
        sock_to_info[sock] = SocketInfo(
            req=json.dumps(dict(page=page_name)),
            resp=[],  # to store bytes we receive
            page_name=page_name
        )

    writeables = sock_to_info.keys()
    readables = sock_to_info.keys()
    while len(writeables) > 0 or len(readables) > 0:

        rlist, wlist, xlist = select.select(readables, writeables, ())
        assert len(xlist) == 0, "Got exceptions on sockets."

        for sock in wlist:
            socket_info = sock_to_info[sock]
            req = socket_info.req
            new_req = comm_nonblock.send(sock, req)

            if new_req is None:
                writeables.remove(sock)
                continue

            socket_info.req = new_req

        for sock in rlist:
            socket_info = sock_to_info[sock]
            data_list = socket_info.resp
            data_part = comm_nonblock.recv(sock)

            if data_part is None:
                handle_response(socket_info.page_name, data_list)
                readables.remove(sock)
                continue
            if len(data_part) > 0:
                data_list.append(data_part)

            socket_info.resp = data_list


def handle_response(page_name, resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password for {}: {}".format(page_name, resp['ok'])

if __name__ == '__main__':
    main()
