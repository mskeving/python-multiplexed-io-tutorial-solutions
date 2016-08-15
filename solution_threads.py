import threading
import comm
import comm_block


ROOT = ""
URLS_FOUND = set()


def get_pw(page_name):
    resp = comm_block.rpc_json(comm.PASSWORD_SERVER, dict(page=page_name))

    if 'ok' not in resp:
        raise Exception("password server said: {!r}".format(resp))

    page_password = resp['ok']

    return page_password


def print_pages(page_name, page_password, alread_seen, start=False):
    resp = comm_block.rpc_json(comm.LINK_SERVER,
                               dict(page=page_name, password=page_password))

    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    links = resp['ok']

    for i, linked_page_name in enumerate(links):
        URLS_FOUND.add(linked_page_name)

        if linked_page_name not in alread_seen:
            print linked_page_name

            alread_seen.append(linked_page_name)
            new_pw = get_pw(linked_page_name)

            thread = threading.Thread(
                target=print_pages,
                args=(linked_page_name, new_pw, alread_seen)
            )
            thread.start()

            if start:
                thread.join()

    if start:
        print "Number of urls found: {}".format(len(URLS_FOUND))

if __name__ == "__main__":
    root_pw = get_pw(ROOT)
    print_pages(ROOT, root_pw, [ROOT], start=True)
