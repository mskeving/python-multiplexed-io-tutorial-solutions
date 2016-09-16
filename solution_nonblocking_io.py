import json
import select

import comm
import comm_nonblock


PASSWORD_SERVER = comm.PASSWORD_SERVER
LINK_SERVER = comm.LINK_SERVER
ROOT_PAGE = ""


class SocketInfo():
    def __init__(self, page_name, req, resp, server):
        self.page_name = page_name
        self.req = req
        self.resp = resp
        self.server = server


def main():
    all_urls = set([ROOT_PAGE])
    sock, socket_info = get_socket_and_info(PASSWORD_SERVER, ROOT_PAGE)

    sock_to_socket_info = {
        sock: socket_info
    }

    writeables = [sock]
    readables = [sock]

    while len(writeables) > 0 or len(readables) > 0:

        rlist, wlist, xlist = select.select(readables, writeables, ())
        assert len(xlist) == 0, "Got exceptions on sockets."

        # write data
        for sock in wlist:
            socket_info = sock_to_socket_info[sock]
            req = socket_info.req
            new_req = comm_nonblock.send(sock, req)

            if new_req is None:
                writeables.remove(sock)
                continue

            socket_info.req = new_req

        # read data
        for sock in rlist:
            socket_info = sock_to_socket_info[sock]
            data_list = socket_info.resp
            data_part = comm_nonblock.recv(sock)

            if data_part is None:
                # we have everything from this socket.

                if socket_info.server == PASSWORD_SERVER:
                    # if we have a new password, we can get new links with it.

                    password = format_resp(data_list)

                    new_sock, new_socket_info = get_socket_and_info(
                        LINK_SERVER, socket_info.page_name, password
                    )
                    sock_to_socket_info[new_sock] = new_socket_info
                    readables.append(new_sock)
                    writeables.append(new_sock)

                elif socket_info.server == LINK_SERVER:
                    # We have a new set of links.
                    links = format_resp(socket_info.resp)
                    new_urls = get_new_urls(links, all_urls)
                    all_urls.update(new_urls)

                    for url in new_urls:
                        print url

                        # get passwords for the new links.
                        new_sock, new_socket_info = get_socket_and_info(
                            PASSWORD_SERVER, url
                        )
                        sock_to_socket_info[new_sock] = new_socket_info
                        readables.append(new_sock)
                        writeables.append(new_sock)

                readables.remove(sock)
                continue

            if len(data_part) > 0:
                data_list.append(data_part)

            socket_info.resp = data_list


def get_socket_and_info(server, page_name, password=None):
    sock = comm_nonblock.connect(server)

    # PASSWORD_SERVER doesn't care if we pass password=None
    req = dict(page=page_name, password=password)

    socket_info = SocketInfo(
        req=json.dumps(req),
        resp=[],  # to store bytes we receive
        page_name=page_name,
        server=server,
    )

    return sock, socket_info


def format_resp(resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    return resp['ok']


def get_new_urls(links, all_urls):
    new_urls = []

    for linked_page_name in links:
        if linked_page_name not in all_urls:
            new_urls.append(linked_page_name)

    return new_urls


if __name__ == '__main__':
    main()
