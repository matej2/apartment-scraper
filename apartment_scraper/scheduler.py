import os
import sys

import django
import requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from webdriverdownloader import GeckoDriverDownloader
import asyncio




def get_driver():
    GECKO_VER = 'v0.26.0'
    gdd = GeckoDriverDownloader()
    driver_path = gdd.get_download_path(GECKO_VER)
    if os.path.isdir(driver_path) and len(os.listdir(driver_path)) == 0:
        gdd.download_and_install(GECKO_VER)

def notify(str):
    requests.post(os.environ['DISCORD_WH'], data={
        'content': str
    })


def my_except_hook(exctype, value, traceback):
    notify(f'{exctype}: {value} | {traceback}')

sys.excepthook = my_except_hook

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
    django.setup()

    from scraper.common import main
    get_driver()
    scheduler.add_job(main, trigger=IntervalTrigger(hours=3))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass