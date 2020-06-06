# apartment-scraper

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