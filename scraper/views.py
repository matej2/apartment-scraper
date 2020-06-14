from __future__ import print_function

import os
import os.path
import pickle

from django.contrib.sites import requests
from django.http import HttpResponse, JsonResponse
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from rest_framework.decorators import api_view
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from apartment_scraper import settings
# Create your views here.
from scraper.models import Apartment

SCOPES = ['https://www.googleapis.com/auth/contacts']

def init_ff():
    binary_dir = os.path.abspath(os.path.join('target', 'geckodriver.exe'))
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options, firefox_profile=firefox_profile, executable_path=binary_dir)
    return driver


def scrape_params(request):
    driver = init_ff()

    # Make sure that list ordering is 'by latest'
    for listing in settings.POST_LISTING:
        driver.get(listing)
        post_list = driver.find_elements_by_css_selector('.seznam [itemprop*=name] a')

        for post in post_list:
            link = post.get_attribute('href')
            if len(Apartment.objects.filter(url=link)) == 0:
                post = Apartment(url=link)
                post.save()
                print('Added')
            else:
                print('Not added, stopping')
                break

    driver.close()
    return JsonResponse(status=200)


def process_parameters(request):
    unscraped_posts = Apartment.objects.filter(status = 0)
    post_container_sel = '#podrobnosti'

    if len(unscraped_posts) == 0:
        return HttpResponse('Nothing to do', status=200)

    driver = init_ff()


    print(f'unscraped:{len(unscraped_posts)}')

    for post in unscraped_posts:
        driver.get(post.url)
        phone_nums = driver.find_element_by_css_selector(f'{post_container_sel} .kontakt-opis a[href*=tel]').text
        rent = driver.find_element_by_css_selector(f'{post_container_sel} .cena').text
        title = driver.find_element_by_css_selector(f'{post_container_sel} #opis .kratek .rdeca').text

        curr_post = Apartment.objects.get(pk=post.id)
        curr_post.contact = phone_nums
        curr_post.title = title
        curr_post.rent = rent
        curr_post.status = 1
        curr_post.save()

    driver.close()
    return JsonResponse(status=200)


def add_contact(request):
    creds = None

    unscraped_posts = Apartment.objects.filter(status=1)
    notify(len(unscraped_posts))

    if len(unscraped_posts) == 0:
        return HttpResponse('Nothing to do', status=200)

    print(f'unscraped:{len(unscraped_posts)}')


    # The file token.pickle is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('people', 'v1', credentials=creds)

    for post in unscraped_posts:
        curr_post = Apartment.objects.get(pk=post.id)

        service.people().createContact(body={
            "names": [
                {
                    "givenName": curr_post.title
                }
            ],
            "phoneNumbers": [
                {
                    'value': curr_post.contact
                }
            ],
            "biographies": [
                {
                    "value": f"Rent: {curr_post.rent}"
                }
            ],
            "urls": [
                {
                    "value": curr_post.url
                }
            ]
        }).execute()
        Apartment.objects.get(pk=post.id).delete()

    return HttpResponse('ok', status=200)


@api_view(['GET'])
def apartment_list_view(request):
    return JsonResponse({
        'apartments': list(Apartment.objects.all().values())
    }, status=200)


def notify(updated_cnt):
    if updated_cnt > 0:
        for wh in settings.DISCORD_WH:
            requests.post(wh, data={
                'content': f'Updated {updated_cnt} posts'
            })
