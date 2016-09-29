import json

import comm_nonblock
import ev

from comm import PASSWORD_SERVER, LINK_SERVER
from comm_ev import send_recv


def format_resp(resp):
    data = b''.join(resp)

    resp = json.loads(data)
    if 'ok' not in resp:
        raise Exception("server said: {!r}".format(resp))

    return resp['ok']


def crawl(event_loop):
    all_urls = set([""])

    def fetch(page_name):
        req = json.dumps(dict(page=page_name))
        sock = comm_nonblock.connect(PASSWORD_SERVER)

        send_recv(event_loop, sock, req, lambda resp: request_urls(resp))

        def request_urls(resp):
            password = format_resp(resp)
            req = json.dumps(dict(page=page_name, password=password))
            sock = comm_nonblock.connect(LINK_SERVER)

            send_recv(event_loop, sock, req, lambda resp: print_urls(resp))

            def print_urls(resp):
                links = format_resp(resp)
                for link in links:
                    if link not in all_urls:
                        print link
                        all_urls.add(link)
                        fetch(link)

    fetch("")
    return all_urls


if __name__ == '__main__':
    event_loop = ev.EventLoop()

    found = crawl(event_loop)

    event_loop.run()

    print "total: {}".format(len(found))
