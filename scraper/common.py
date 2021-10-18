import os
import random
import time
from urllib.parse import urlparse, urljoin

import django
from bs4 import BeautifulSoup

from apartment_scraper.proxy import get_using_headers
from scraper.GoogleUtilities import add_contact

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment
from notify import DEV_PIC, notify


def add_contacts():
    result = True
    for a in Apartment.objects.filter(status=1):
        result = result and add_contact(a)

def get_post_links(soup, listing):
    link_list = []

    domain = urlparse(listing.url).netloc
    scheme = urlparse(listing.url).scheme
    base = scheme + '://' + domain

    for post in soup.select(listing.post_link_list_selector):
        if post is not None and post['href'] is not None:
            link_list.append(urljoin(base, post['href']))
    return link_list

def get_posts(link_list):
    post_list = []

    for link in link_list:

        if len(Apartment.objects.filter(url=link)) == 0:
            response = get_using_headers(link)
            # If no response, skip
            if response is None:
                continue

            post_list.append(response)

    return post_list

def main_updated():
    if len(Listing.objects.all()) == 0:
        print('No listings, skipping')
        return True

    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()

    # Get search page
    for listing in listings:


        # If website does not return 200, try changing last attr to true (use proxy)
        response = get_using_headers(listing.url)

        if response is None:
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get post links
        link_list = get_post_links(soup, listing)

        # Get posts
        post_list = get_posts(link_list)

        for post in post_list:
            soup = BeautifulSoup(post.content, 'html.parser')
            post_sel = listing.post_container_selector

            # Scrape attributes
            url = post.url
            phone_nums = soup.select_one(f'{post_sel} {listing.contact_selector}')
            rent = soup.select_one(f'{post_sel} {listing.rent_selector}')
            title = soup.select_one(f'{post_sel} {listing.title_selector}')
            description = soup.select_one(f'{post_sel} {listing.description_selector}')
            picture = soup.select_one(f'{post_sel} {listing.picture_selector}')

            if phone_nums is not None:
                phone_nums = phone_nums.getText().strip()
            else:
                phone_nums = ''
            if rent is not None:
                rent = rent.getText().strip()
            else:
                rent = ''
            if title is not None:
                title = title.getText().strip()
            else:
                title = ''
            if description is not None:
                description = description.getText(separator="\n").strip()
            else:
                description = '(Not found)'
            if picture is not None:
                if urlparse(picture.attrs.get('href', '')).netloc != '':
                    picture = urlparse(picture.attrs.get('href', DEV_PIC)).geturl()
                else:
                    picture = urlparse(picture.attrs.get('src', DEV_PIC)).geturl()
            else:
                picture = DEV_PIC

            print(f'New post: {title}')

            # Update or create Picture
            try:
                curr_post = Apartment.objects.get(url=post)
            except Apartment.DoesNotExist:
                curr_post = Apartment()

            curr_post.contact = phone_nums[:254]
            curr_post.title = title[:243]
            curr_post.rent = rent[:254]
            curr_post.status = 1
            curr_post.description = description[:499]
            curr_post.picture_url = picture
            curr_post.url = url
            curr_post.save()

            notify(listing, curr_post)
            time.sleep((random.random() * 1000 + 1000) / 1000)

    return True

