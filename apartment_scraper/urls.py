"""apartment_scraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from scraper.views import scrape_params, process_parameters, add_contact, run_all
from scraper import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'parameters', views.ProductRESTView)

urlpatterns = [
    url('parameters/scrape', scrape_params),
    url('parameters/process', process_parameters),
    url('parameters/save', add_contact),
    url('parameters/run_all', run_all),
    url(r'^admin/', admin.site.urls),
    url('api/auth', obtain_auth_token),
    path('api/', include(router.urls)),
]
