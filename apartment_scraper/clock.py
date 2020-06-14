from apscheduler.schedulers.blocking import BlockingScheduler
from scraper.views import scrape_params,process_parameters,add_contact
sched = BlockingScheduler()


@sched.scheduled_job('interval', hours=3)
def timed_job():
    print('This job is run every three minutes.')
    scrape_params(None)
    process_parameters(None)
    add_contact(None)


sched.start()