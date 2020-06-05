from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
from django.http import HttpResponse

# Create your views here.
from scraper.models import Apartment


def scrape_params(request):
    #binary_dir = os.path.join('opt', 'geckodriver')
    #binary = FirefoxBinary(binary_dir)

    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    options = Options()
    options.headless = True
    options.preferences.update({"javascript.enabled": False})
    driver = webdriver.Firefox(options=options)

    # Make sure that list ordering is 'by latest'
    driver.get("https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/ljubljana-bezigrad,ljubljana-moste-polje/stanovanje/garsonjera,1-sobno,1.5-sobno/?s=16")

    post_url_list = driver.find_elements_by_css_selector('.seznam [itemprop*=name] a')

    for link in post_url_list:
        post = Apartment(url=link.get_attribute('href'), scraped=False)
        post.save()

    driver.close()
    return HttpResponse('ok check', status=200)
