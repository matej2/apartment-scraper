from django.views.generic import ListView
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
from django.http import HttpResponse

# Create your views here.
from scraper.models import Apartment


def scrape_params(request):
    # binary_dir = os.path.join('opt', 'geckodriver')
    # binary = FirefoxBinary(binary_dir)

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options)

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

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options)


    print(f'unscraped:{len(unscraped_posts)}')

    for post in unscraped_posts:
        driver.get(post.url)
        phone_nums = driver.find_element_by_css_selector(f'{post_container_sel} .kontakt-opis a[href*=tel]').text
        title = driver.find_element_by_css_selector('.podrobnosti-naslov').text
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

class ApartmentListView(ListView):
    model = Apartment
    context_object_name = 'apartments'
