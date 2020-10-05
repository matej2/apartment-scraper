import json
import os
from random import choice

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from apartment_scraper.header import get_random_headers

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


def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = BeautifulSoup(response.content, features='html.parser')

    return {'https': 'http://' + choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, soup.select('#proxylisttable td')[::8]),
            map(lambda x: x.text, soup.select('#proxylisttable td')[1::8]))))))}


def requests_retry_session(
        retries=2,
        backoff_factor=0,
        status_forcelist=0,
        session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_using_proxy(url, proxy, c=10):
    while c > 0:
        try:
            c = c - 1
            if proxy is None:
                proxy = proxy_generator()
            header = get_random_headers()
            print('Using proxy {}, c={} to reach {}'.format(proxy, c, url))
            response = requests.get(url, timeout=10, proxies=proxy, headers=header)
            if response.status_code == 200:
                print('Pass in {}-nth try'.format(c))
                return response
        except:
            print('Failed, invalidating proxy')
            proxy = None
