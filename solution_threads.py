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


def get_urls(page_name, urls_found, threads=[]):
    password = get_pw(page_name)
    resp = comm_block.rpc_json(comm.LINK_SERVER,
                               dict(page=page_name, password=password))

    if 'ok' not in resp:
        raise Exception("link server said: {!r}".format(resp))

    links = resp['ok']

    for linked_page_name in links:
        if linked_page_name not in urls_found:
            print linked_page_name

            urls_found.add(linked_page_name)

            thread = threading.Thread(
                target=get_urls,
                args=(linked_page_name, urls_found, threads)
            )
            thread.start()

            threads.append(thread)

    return urls_found, threads

if __name__ == "__main__":
    urls_found, threads = get_urls(ROOT, set([ROOT]))

    for thread in threads:
        thread.join()

    print "{} total urls found".format(len(urls_found))
