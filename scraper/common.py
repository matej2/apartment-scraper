import json
import os
import re
from urllib.parse import urlparse, urljoin

import django
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from requests import get

from apartment_scraper.proxy import proxy_generator, get_using_headers
from scraper.GoogleUtilities import add_contact

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.models import Listing, Apartment

try:
    ua = UserAgent()
except:
    ua = 'Mozilla/5.0 (Android; Mobile; rv:40.0)'

proxy = proxy_generator()

def notify(txt, ap):
    print(txt)
    headers = {'Content-Type': 'application/json'}

    data = {}
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = str(txt)
    #data["username"] = "Apartment Scraper bot"

    # leave this out if you dont want an embed
    data["embeds"] = []
    embed = {
        "image": {
            "url": str(ap.picture_url)
        }
    }
    # for all params, see https://discordapp.com/developers/docs/resources/channel#embed-object
    data["embeds"].append(embed)

    if "DISCORD_WH" in os.environ:
        result = requests.post(os.getenv('DISCORD_WH'), data=json.dumps(data), headers={"Content-Type": "application/json"})

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))
    else:
        print('DISCORD_WH missing, skipping')


def main():
    link_list = []

    if len(Listing.objects.all()) == 0:
        print('No listings, skipping')
        return True

    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()

    # Get search page
    for listing in listings:
        domain = urlparse(listing.url).netloc
        scheme = urlparse(listing.url).scheme
        base = scheme + '://' + domain

        # If website does not return 200, try changing last attr to true (use proxy)
        response = get_using_headers(listing.url, proxy, False)

        if response is None:
            print('No response for listing: {}'.format(listing.url))
            continue

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get post links
        for post in soup.select(listing.post_link_list_selector):
            if post is not None and post['href'] is not None:
                link_list.append(urljoin(base, post['href']))

        # Get posts
        for link in link_list:

            if len(Apartment.objects.filter(url=link)) == 0:
                post_sel = listing.post_container_selector
                response = get_using_headers(link, proxy, False)

                if response is None:
                    print('No response for post {}'.format(link))
                    continue

                soup = BeautifulSoup(response.content, 'html.parser')

                # Scrape attributes
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
                    #description = description.replace('\n', '')
                    #description = description.replace('\t', '')
                else:
                    description = '(Not found)'
                if picture is not None:
                    if urlparse(picture.attrs.get('href', '')).netloc != '':
                        picture = urlparse(picture.attrs.get('href', ''))
                    else:
                        picture = urlparse(picture.attrs.get('src', ''))
                else:
                    picture = 'https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/No_picture_available.png/160px-No_picture_available.png'

                # Save attributes
                # Update or create Picture
                try:
                    curr_post = Apartment.objects.get(url=link)
                except Apartment.DoesNotExist:
                    curr_post = Apartment()

                curr_post.contact = phone_nums[:254]
                curr_post.title = title[:243]
                curr_post.rent = rent[:254]
                curr_post.status = 1
                curr_post.description = description[:499]
                curr_post.picture_url =picture.geturl()
                curr_post.url = link
                curr_post.save()

                #if add_contact(curr_post) is False:
                #    notify('Error adding')


                notify(f"""
New post: [{curr_post.title}]({curr_post.url}) in listing [{domain}]({listing.url})
Rent: {curr_post.rent}
Contact: {curr_post.contact}
Description: 

> {curr_post.description}
                """, curr_post)
        print(f'No more in {listing.url}')
    print(f'Finished')
    return True

def add_contacts():
    result = True
    for a in Apartment.objects.filter(status=1):
        result = result and add_contact(a)
