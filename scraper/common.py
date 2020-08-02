import os
import django
import requests

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

from scraper.GoogleUtilities import add_contact
from webdriverdownloader import GeckoDriverDownloader
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment



def init_ff():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})

    driver_path = os.environ.get('GECKODRIVER_PATH')
    driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile, executable_path=driver_path, firefox_binary=binary)
    return driver


def main():
    get_driver()

    print('Running main')

    if len(Listing.objects.all()) == 0:
        return True

    driver = init_ff()
    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()
    for listing in listings:
        driver.get(listing.url)

        post_cnt = 0
        link_list = [post.get_attribute('href') for post in
                     driver.find_elements_by_css_selector(listing.post_link_list_selector)]

        for link in link_list:

            if len(Apartment.objects.filter(url=link)) == 0:
                post_sel = listing.post_container_selector

                driver.get(link)

                # Scrape attributes
                phone_nums = driver.find_element_by_css_selector(f'{post_sel} {listing.contact_selector}').text
                rent = driver.find_element_by_css_selector(f'{post_sel} {listing.rent_selector}').text
                title = driver.find_element_by_css_selector(f'{post_sel} {listing.title_selector}').text

                # Save attributes
                curr_post = Apartment(url=link)
                curr_post.contact = phone_nums
                curr_post.title = title
                curr_post.rent = rent
                curr_post.status = 1
                curr_post.save()

                if add_contact(curr_post):
                    notify(f'Added new apartment: {curr_post.title} Rent: {curr_post.rent} Contact: {curr_post.contact}')
                else:
                    notify(f'Problem adding {curr_post.title}, phone num: {curr_post.contact}')
                    return False
            else:
                print(f'No more left in listing {listing.url}')
    driver.close()
    return True


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
    if os.environ['DISCORD_WH'] is not None:
        requests.post(os.environ['DISCORD_WH'], data={
            'content': str
        })