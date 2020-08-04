release: python manage.py migrate
web: gunicorn apartment_scraper.wsgi
clock: python apartment_scraper/scheduler.py