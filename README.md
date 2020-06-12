# apartment-scraper

> When I was looking for an apartment, most of the times I had to call to get more information. After a while, I had a lot of contacts and I became confused who is calling.

This is a scraper which reads parameters about apartments from various sites (for example nepremičnine). It then backups any data related to apartment into Google Contacts, so you can have clear and organized communication.

## Installation and setup

1. Clone repository
2. Install  `pipenv`
3. Run `pipenv install` and `pipenv shell`
4. Download geckodriver and put it in `target` directory. Make sure that there is correct executable path in `init_ff()`
4. Inside virtualenv, run `py manage.py runserver`

## Endpoints

GET `/parameters/scrape`
Gets url parameters and saves them to database

GET `/parameters/process`
Reads url parameters from database and gets additional parameters.

GET `/parameters`
See scraped parameters
