import json
import os
from urllib.parse import urlparse

import django
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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


def notify(str, ap):
    print(str)
    headers = {'Content-Type': 'application/json'}

    data = {}
    # for all params, see https://discordapp.com/developers/docs/resources/webhook#execute-webhook
    data["content"] = str
    #data["username"] = "Apartment Scraper bot"

    # leave this out if you dont want an embed
    data["embeds"] = []
    embed = {
        "image": {
            "url": ap.picture_url
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
    proxy = proxy_generator()

    if len(Listing.objects.all()) == 0:
        print('No new listings, skipping')
        return True


    # Make sure that list ordering is 'by latest'
    listings = Listing.objects.all()

    for listing in listings:
        response = get_using_proxy(listing.url, proxy)

        if response is None:
            print('No response for listing: {}'.format(listing.url))
            continue

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
                if soup.select_one(f'{post_sel} {listing.contact_selector}') is not None:
                    phone_nums = soup.select_one(f'{post_sel} {listing.contact_selector}').getText()
                else:
                    phone_nums = ''
                if soup.select_one(f'{post_sel} {listing.rent_selector}') is not None:
                    rent = soup.select_one(f'{post_sel} {listing.rent_selector}').getText()
                else:
                    rent = ''
                title = soup.select_one(f'{post_sel} {listing.title_selector}').getText()
                if listing.description_selector is not None and listing.description_selector != '':
                    try:
                        description = soup.select_one(f'{post_sel} {listing.description_selector}').getText()
                        description = description.replace('\n', '')
                        description = description.replace('\t', '')
                    except:
                        print('Description not found')
                if listing.picture_selector != '':
                    picture = o = urlparse(soup.select_one(f'{post_sel} {listing.picture_selector}').attrs.get('href', ''))
                else:
                    picture = ''

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

                notify(f"""
New apartment: [{curr_post.title}]({curr_post.url}) in listing [{domain}]({listing.url})
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
