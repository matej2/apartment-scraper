from django.db import models

# Create your models here.
from django.utils import timezone


class Apartment(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=244, null=True)
    rent = models.CharField(max_length=255, null=True)
    contact = models.CharField(max_length=255, null=True)
    status = models.SmallIntegerField(null=True, default=0)
    created = models.DateField(null=True, default=timezone.now)

    def __str__(self):
        return self.url

    class Meta:
        app_label = 'apt'

class Listing(models.Model):
    url = models.CharField(max_length=500)
    limit = models.IntegerField(null=True, default=0)
    post_link_list_selector = models.CharField(max_length=255, default='')
    post_container_selector = models.CharField(max_length=255, default='')
    title_selector = models.CharField(max_length=255, default='')
    rent_selector = models.CharField(max_length=255, default='')
    contact_selector = models.CharField(max_length=255, default='')

    class Meta:
        app_label = 'apt'
