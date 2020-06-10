from __future__ import print_function
from django.views.generic import ListView
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
from django.http import HttpResponse
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

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
    driver.get(
        "https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/ljubljana-bezigrad,ljubljana-moste-polje/stanovanje/garsonjera,1-sobno,1.5-sobno/?s=16")

    post_url_list = driver.find_elements_by_css_selector('.seznam [itemprop*=name] a')

    for link in post_url_list:
        if len(Apartment.objects.filter(url=link.get_attribute('href'))) == 0:
            post = Apartment(url=link.get_attribute('href'), scraped=False)
            post.save()
            print('Added')
        else:
            print('Not added')

    driver.close()
    return HttpResponse('ok check', status=200)


def process_parameters(request):
    unscraped_posts = Apartment.objects.filter(scraped=False)
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
        curr_post.scraped = True
        curr_post.save()

    driver.close()
    return HttpResponse('ok check', status=200)


def add_contact(request):
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
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

    # Call the People API
    print('Insert new contact')
    service.people().createContact(body={
        "names": [
            {
                "givenName": "Samkit"
            }
        ],
        "phoneNumbers": [
            {
                'value': "8600086024"
            }
        ],
        "emailAddresses": [
            {
                'value': 'samkit5495@gmail.com'
            }
        ]
    }).execute()
    return HttpResponse('ok', status=200)

class ApartmentListView(ListView):
    model = Apartment
    context_object_name = 'apartments'
