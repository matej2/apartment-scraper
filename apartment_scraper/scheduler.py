from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apartment_scraper.settings")
django.setup()
from scraper.common import main

if __name__ == '__main__':
    scheduler = BlockingScheduler()

    scheduler.add_job(main, trigger=IntervalTrigger(hours=3))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass