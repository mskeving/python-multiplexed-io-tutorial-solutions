import threading
import comm
import comm_block


ROOT = ""


def get_pw(page_name):
    resp = comm_block.rpc_json(comm.PASSWORD_SERVER, dict(page=page_name))

    if 'ok' not in resp:
        raise Exception("password server said: {!r}".format(resp))

    page_password = resp['ok']

    return page_password


def get_new_urls(links, all_urls):
    new_urls = []

    for linked_page_name in links:
        if linked_page_name not in all_urls:
            print linked_page_name

            new_urls.append(linked_page_name)

    return new_urls


def get_urls(page_name, prev_urls, lock):
    all_urls = prev_urls

    password = get_pw(page_name)
    resp = comm_block.rpc_json(comm.LINK_SERVER,
                               dict(page=page_name, password=password))

    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    links = resp['ok']

    with lock:
        new_urls = get_new_urls(links, all_urls)

        all_urls.update(new_urls)

    threads = []
    for url in new_urls:
        thread = threading.Thread(
            target=get_urls,
            args=(url, all_urls, lock)
        )
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return all_urls

if __name__ == "__main__":
    lock = threading.Lock()

    urls_found = get_urls(ROOT, set([ROOT]), lock)

    print "{} total urls found".format(len(urls_found))
