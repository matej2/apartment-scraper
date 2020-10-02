import json
import os
from random import choice

from scraper.common import init_ff

dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "proxies.json")


def get_proxies():
    driver = init_ff()
    driver.get("https://www.sslproxies.org")
    table = driver.find_element_by_id('proxylisttable')
    proxies = list(
        map(lambda x: x[0] + ':' + x[1],
            list(zip(
                map(lambda x: x.text, table.find_elements_by_tag_name('td')[::8]),
                map(lambda x: x.text, table.find_elements_by_tag_name('td')[1::8])
                )
            )
        )
    )

    return proxies


def save_proxies():
    proxies = get_proxies()

    with open(dir_path, "w") as file:
        file.write(json.dumps(proxies))
    return True


def get_proxy_from_file():
    with open(dir_path, "r") as file:
        return 'https:' + choice(json.loads(file.read()))


def get_proxy():
    return 'https:' + choice(get_proxies())