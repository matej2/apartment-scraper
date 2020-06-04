from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import os
from django.http import HttpResponse

# Create your views here.


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
    driver.get("https://www.freecodecamp.org/the-fastest-web-page-on-the-internet")

    title = driver.find_element_by_tag_name('h1').text

    driver.close()
    return HttpResponse(title, status=200)
