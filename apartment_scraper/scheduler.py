import asyncio
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from scraper.common import main, notify


def my_except_hook(exctype, value, traceback):
    notify(f'{exctype}: {value} | {traceback}')

sys.excepthook = my_except_hook

if __name__ == '__main__':
    scheduler = BlockingScheduler()

    scheduler.add_job(main, trigger=IntervalTrigger(minutes=35))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass