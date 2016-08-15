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


def print_pages(page_name, page_password, already_seen, start=False):
    resp = comm_block.rpc_json(comm.LINK_SERVER,
                               dict(page=page_name, password=page_password))

    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    links = resp['ok']

    for linked_page_name in links:
        URLS_FOUND.add(linked_page_name)

        if linked_page_name not in already_seen:
            print linked_page_name

            already_seen.append(linked_page_name)
            new_pw = get_pw(linked_page_name)

            print_pages(linked_page_name, new_pw, already_seen)

    if start:
        print len(URLS_FOUND)


if __name__ == "__main__":
    root_pw = get_pw(ROOT)
    print_pages(ROOT, root_pw, [ROOT], start=True)
