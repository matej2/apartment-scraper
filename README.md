# apartment-scraper

> When I was looking for an apartment, most of the times I had to call to get more information. After a while, I had a lot of contacts and I became confused who is contacting me.

This is a scraper which reads parameters about apartments from various sites (for example [nepremicnine](https://www.nepremicnine.net/)). It then backups any data related to apartment into Google Contacts and database, so you can have clear and organized communication.

## Installation and setup

1. Clone repository
2. Install  `pipenv`
3. Run `pipenv shell` and `pipenv install`
4. Inside pipenv, run `py manage.py runserver` or `python3 manage.py runserver`
5. You can then [create superuser](https://djangocentral.com/creating-super-user-in-django/) to add other users and config
6. Create an app in [Google console](https://developers.google.com/people/quickstart/python#step_1_turn_on_the) and save credentials in app root as `credentials.json`

You can then either [import](https://docs.djangoproject.com/en/3.0/ref/django-admin/#loaddata) scrape settings from `scraper/fixtures` or create your own. Driver is installed automatically. 

## Endpoints

GET `api/auth`
Obtain authentication token.

Request body:
```
{
  'username': <name>,
  'password': <pass>
}
```

GET `/parameters/run_all`
See scraped parameters

Headers: `Authentication: Token <token>`

## Contributing

You are welcome to help! Check out issues that are not being worked on and assign yourself (or leave a comment). Open a separate branch and PR so we can review your changes.