import json
import os
import random
import time
from random import choice

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from apartment_scraper.header import get_random_headers


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
            time.sleep((random.random() * 1000 + 1000) / 1000)
            response = requests.get(url, timeout=10, proxies=proxy, headers=header)
            if response.status_code == 200:
                print('Pass in {}-nth try'.format(c))
                return response
        except:
            print('Failed, invalidating proxy')
            proxy = None
    return None