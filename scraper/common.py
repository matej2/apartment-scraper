import os
from random import choice
from urllib.parse import urlparse

import django
import requests
from fake_useragent import UserAgent
from http_request_randomizer.requests.proxy.requestProxy import RequestProxy
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from webdriverdownloader import GeckoDriverDownloader

from scraper.GoogleUtilities import add_contact

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment

try:
    ua = UserAgent()
except:
    ua = 'Mozilla/5.0 (Android; Mobile; rv:40.0)'

PROXY_LIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apartment_scraper",
                          "proxies.json")


def init_ff(proxy):
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    if os.path.exists(PROXY_LIST):
        firefox_profile.set_preference("general.useragent.override", ua.random)

    if os.environ.get('FIREFOX_BIN') is not None:
        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    else:
        binary = FirefoxBinary()

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})

    if os.environ.get('GECKODRIVER_PATH') is None:
        print('Driver not installed')
    else:
        driver_path = os.environ.get('GECKODRIVER_PATH')

    if proxy is not None:
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": proxy,
            "ftpProxy": proxy,
            "sslProxy": proxy,
            "proxyType": "MANUAL",
        }

    driver = webdriver.Firefox(
        options=options,
        firefox_profile=firefox_profile,
        executable_path=driver_path,
        firefox_binary=binary)

    driver.implicitly_wait(10)
    return driver


def get_driver():
    GECKO_VER = 'v0.26.0'
    download_dir = os.path.abspath('target')

    if os.environ.get('GECKODRIVER_PATH') is None:
        if os.path.isdir(download_dir) is False:
            os.mkdir(download_dir)
        gdd = GeckoDriverDownloader(download_root=download_dir)
        driver_path = gdd.get_download_path(GECKO_VER)
        if os.path.isdir(driver_path) is False:
            path = gdd.download_and_install(GECKO_VER)
            os.environ["GECKODRIVER_PATH"] = str(path[0])


def notify(str):
    print(str)
    if os.environ['DISCORD_WH'] is not None:
        requests.post(os.environ['DISCORD_WH'], data={
            'content': str
        })
        print('Message sent')
    else:
        print('DISCORD_WH missing, skipping')


# Updated script from: https://zenscrape.com/how-to-build-a-simple-proxy-rotator-in-python/
def proxy_generator():
    driver = init_ff(None)
    driver.get("https://sslproxies.org/")
    ip_list = driver.find_elements_by_css_selector('#proxylisttable td')[::8]
    port_list = driver.find_elements_by_css_selector('#proxylisttable td')[1::8]

    driver.close()

    return choice(list(map(lambda x: x[0] + ':' + x[1], list(
        zip(map(lambda x: x.text, ip_list),
            map(lambda x: x.text, port_list))))))


def main():
    notify('Running main')
    proxy = proxy_generator()

    get_driver()
    if len(Listing.objects.all()) == 0:
        print('No new listings, skipping')
        return True

    driver = init_ff(proxy)
    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()
    for listing in listings:
        driver.get(listing.url)
        domain = urlparse(listing.url).netloc

        post_cnt = 0
        link_list = [post.get_attribute('href') for post in
                     driver.find_elements_by_css_selector(listing.post_link_list_selector)]

        for link in link_list:

            if len(Apartment.objects.filter(url=link)) == 0:
                post_sel = listing.post_container_selector

                driver.get(link)

                # Scrape attributes
                description = ''
                phone_nums = driver.find_element_by_css_selector(f'{post_sel} {listing.contact_selector}').text
                rent = driver.find_element_by_css_selector(f'{post_sel} {listing.rent_selector}').text
                title = driver.find_element_by_css_selector(f'{post_sel} {listing.title_selector}').text
                if listing.description_selector is not None and listing.description_selector != '':
                    try:
                        description = driver.find_element_by_css_selector(
                            f'{post_sel} {listing.description_selector}').text
                        description = description.replace('\n', '')
                        description = description.replace('\t', '')
                    except:
                        print('Description not found')

                # Save attributes
                curr_post = Apartment(url=link)
                curr_post.contact = phone_nums
                curr_post.title = title
                curr_post.rent = rent
                curr_post.status = 1
                curr_post.description = description
                curr_post.save()

                result = add_contact(curr_post)
                # add_picture(result, )

                if result:
                    notify(f"""
New apartment: [{curr_post.title}]({curr_post.url}) in listing [{domain}]({listing.url})
Rent: {curr_post.rent}
Contact: {curr_post.contact}
Description: 

> {curr_post.description}
                    """)
                else:
                    notify(f'Problem adding {curr_post.title}, phone num: {curr_post.contact}')
                    return False
        print(f'No more in {listing.url}')
    driver.close()
    print(f'Finished')
    return True
