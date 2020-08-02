import asyncio
import sys

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from scraper.common import main, notify


def my_except_hook(exctype, value, traceback):
    notify(f'{exctype}: {value} | {traceback}')

sys.excepthook = my_except_hook

if __name__ == '__main__':
    scheduler = AsyncIOScheduler()

    scheduler.add_job(main, trigger=IntervalTrigger(seconds=30))

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass