import json
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
    while len(sock_to_req) > 0:
        for sock in sock_to_req.keys():
            req = sock_to_req.pop(sock)

            new_req = comm_nonblock.send(sock, req)

            if new_req is not None:
                sock_to_req[sock] = new_req

    # read all requests
    while len(sock_to_resp) > 0:
        for sock in sock_to_resp.keys():

            data_list = sock_to_resp.pop(sock)
            data_part = comm_nonblock.recv(sock)

            if data_part is None:
                # We're done.
                handle_response(data_list)
            else:
                if len(data_part) > 0:
                    data_list.append(data_part)

                # There still might be more coming.
                sock_to_resp[sock] = data_list


def handle_response(resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    print "password: {}".format(resp['ok'])

if __name__ == '__main__':
    main()
