import requests
from apscheduler.schedulers import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apartment_scraper import settings


if __name__ == '__main__':
    scheduler = AsyncIOScheduler()
    scheduler.add_job(main, trigger=IntervalTrigger(hours=3))

    notification = ""
    for job in scheduler.get_jobs():
        notification += job.func_ref + str(job.trigger.interval) + ', '

    scheduler.start()
    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass