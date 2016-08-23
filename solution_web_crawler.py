import comm
import comm_block


ROOT = ""


def get_pw(page_name):
    resp = comm_block.rpc_json(comm.PASSWORD_SERVER, dict(page=page_name))

    if 'ok' not in resp:
        raise Exception("password server said: {!r}".format(resp))

    page_password = resp['ok']

    return page_password


def get_urls(page_name, urls_found):
    password = get_pw(page_name)
    resp = comm_block.rpc_json(comm.LINK_SERVER,
                               dict(page=page_name, password=password))

    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    links = resp['ok']

    for linked_page_name in links:
        if linked_page_name not in urls_found:
            urls_found.add(linked_page_name)
            new_urls = get_urls(linked_page_name, urls_found)
            urls_found.update(new_urls)

    return urls_found


if __name__ == "__main__":
    urls_found = get_urls(ROOT, set([ROOT]))

    for url in urls_found:
        print url

    print "{} total urls found".format(len(urls_found))
