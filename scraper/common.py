import os
import random
import re
import time
from urllib.parse import urlparse, urljoin

import django
from bs4 import BeautifulSoup

from apartment_scraper.proxy import get_using_headers
from scraper.GoogleUtilities import add_contact

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment, Photo
from .notify import send_discord_wh


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

def clean(str):
    return re.sub('(\\n)+', '\n', str.replace('Izračun kredita', ''))

def main():
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
            picture = soup.select(f'{post_sel} {listing.picture_selector}')
            description_2 = soup.select_one(f'{post_sel} {listing.description_2_selector}')
            subtitle = soup.select_one(f'{post_sel} {listing.subtitle_selector}')

            if phone_nums is not None:
                phone_nums = clean(phone_nums.getText().strip())
            else:
                phone_nums = ''
            if rent is not None:
                rent = clean(rent.getText().strip())
            else:
                rent = ''
            if title is not None:
                title = clean(title.getText().strip())
            else:
                title = ''
            if description is not None:
                description = description.getText(separator="\n").strip()
            else:
                description = '(Not found)'
            if description_2 is not None:
                description_2 = clean(description_2.getText().strip())
            else:
                description_2 = ''
            if subtitle is not None:
                subtitle = clean(subtitle.getText().strip())
            else:
                subtitle = ''


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
            curr_post.url = url
            curr_post.description_2 = description_2
            curr_post.subtitle = subtitle
            curr_post.save()

            if picture is not None:
                for p in picture:
                    try:
                        post_photo = Photo.objects.get(url=post)
                    except Photo.DoesNotExist:
                        post_photo = Photo()

                    data_url = urlparse(p.attrs.get('href')).geturl()
                    if data_url == b'':
                        data_url = urlparse(p.attrs.get('src')).geturl()
                    if data_url == b'':
                        data_url = urlparse(p.attrs.get('data-src')).geturl()

                    post_photo.url = data_url.replace('thumbnails', '')
                    post_photo.apartment = curr_post
                    post_photo.save()

            send_discord_wh(listing, curr_post)
            time.sleep((random.random() * 1000 + 1000) / 1000)

    return True

