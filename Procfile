release: py manage.py migrate
web: gunicorn apartment_scraper.wsgi
clock: py apartment_scraper/scheduler.py