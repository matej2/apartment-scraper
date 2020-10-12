import os
from urllib.parse import urlparse

import django
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
from webdriverdownloader import GeckoDriverDownloader

from apartment_scraper.header import get_random_headers
from apartment_scraper.proxy import proxy_generator, get_using_proxy
from scraper.GoogleUtilities import add_contact

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment

try:
    ua = UserAgent()
except:
    ua = 'Mozilla/5.0 (Android; Mobile; rv:40.0)'

PROXY_LIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "apartment_scraper", "proxies.json")

def init_ff():
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

    driver = webdriver.Firefox(
        options=options,
        firefox_profile=firefox_profile,
        executable_path=driver_path,
        firefox_binary=binary)
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
    if os.getenv('DISCORD_WH') is not None:
        requests.post(os.environ['DISCORD_WH'], data={
            'content': str
        })
        print('Message sent')
    else:
        print('DISCORD_WH missing, skipping')


def main():
    link_list = []
    proxy = proxy_generator()

    notify('Running main')

    if len(Listing.objects.all()) == 0:
        print('No new listings, skipping')
        return True


    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()

    for listing in listings:
        response = get_using_proxy(listing.url, proxy)
        soup = BeautifulSoup(response.content, 'html.parser')

        domain = urlparse(listing.url).netloc
        scheme = urlparse(listing.url).scheme

        post_cnt = 0
        for post in soup.select(listing.post_link_list_selector):
            if post is not None and post['href'] is not None:
                link_list.append(scheme + '://' + domain + post['href'])


        for link in link_list:

            if len(Apartment.objects.filter(url=link)) == 0:
                post_sel = listing.post_container_selector

                response = get_using_proxy(link, proxy)
                if response is None:
                    print('Return is null, skipping...')
                    continue
                soup = BeautifulSoup(response.content, 'html.parser')

                # Scrape attributes
                description = ''
                phone_nums = soup.select_one(f'{post_sel} {listing.contact_selector}').getText()
                rent = soup.select_one(f'{post_sel} {listing.rent_selector}').getText()
                title = soup.select_one(f'{post_sel} {listing.title_selector}').getText()
                if listing.description_selector is not None and listing.description_selector != '':
                    try:
                        description = soup.select_one(f'{post_sel} {listing.description_selector}').getText()
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
                #add_picture(result, )

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
    print(f'Finished')
    return True