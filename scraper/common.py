import os
import django

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from apartment_scraper import settings
settings.configure()
django.setup()

from scraper.GoogleUtilities import add_contact
from scraper.models import Listing, Apartment



def init_ff():
    binary_dir = os.path.abspath(os.path.join('target', 'geckodriver'))
    print(binary_dir)
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile, executable_path=binary_dir)
    return driver

def main(request=None):

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
                    print(f'Added {curr_post.title}')
                else:
                    print(f'Problem adding {curr_post.title}, phone num: {curr_post.contact}')
            else:
                print(f'No more left in listing {listing.url}')
    driver.close()
    return True