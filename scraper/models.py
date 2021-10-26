from django.db import models

# Create your models here.
from django.utils import timezone


class Apartment(models.Model):
    url = models.CharField(max_length=400)
    title = models.CharField(max_length=244, null=True)
    rent = models.CharField(max_length=255, null=True)
    contact = models.CharField(max_length=255, null=True)
    status = models.SmallIntegerField(null=True, default=0)
    created = models.DateField(null=True, default=timezone.now)
    description = models.CharField(max_length=500, null=True)
    description_2 = models.CharField(max_length=500, null=True)
    subtitle = models.CharField(max_length=250, null=True)

    def __str__(self):
        return f'{self.title}: {self.url}'

class Photo(models.Model):
    url = models.CharField(max_length=400)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.url

class Listing(models.Model):
    url = models.CharField(max_length=2000)
    limit = models.IntegerField(null=True, default=0)
    post_link_list_selector = models.CharField(max_length=255, default='', null=True)
    post_container_selector = models.CharField(max_length=255, default='', null=True)
    title_selector = models.CharField(max_length=255, default='', null=True)
    rent_selector = models.CharField(max_length=255, default='', null=True)
    contact_selector = models.CharField(max_length=255, default='', null=True)
    description_selector = models.CharField(max_length=255, default='', null=True)
    picture_selector = models.CharField(max_length=255, default='', null=True)
    description_2_selector = models.CharField(max_length=255, default='', null=True)
    subtitle_selector = models.CharField(max_length=255, default='', null=True)
