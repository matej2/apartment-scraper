import os
import sys
import requests

from apscheduler.schedulers import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from webdriverdownloader import GeckoDriverDownloader

from scraper.views import run_all


def get_driver():
    GECKO_VER = 'v0.26.0'
    gdd = GeckoDriverDownloader()
    if len(os.listdir(gdd.get_download_path(GECKO_VER))) == 0:
        gdd.download_and_install(GECKO_VER)

def notify(str):
    requests.post(os.environ['DISCORD_WH'], data={
        'content': str
    })


def my_except_hook(exctype, value, traceback):
    if exctype == KeyboardInterrupt:
        print
        "Handler code goes here"
    else:
        sys.__excepthook__(exctype, value, traceback)

sys.excepthook = my_except_hook

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    get_driver()
    scheduler.add_job(run_all, trigger=IntervalTrigger(hours=3))

    notification = ""
    for job in scheduler.get_jobs():
        notification += job.func_ref + str(job.trigger.interval) + ', '

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass