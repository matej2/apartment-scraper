from django.db import models

# Create your models here.
from django.utils import timezone


class Apartment(models.Model):
    url = models.CharField(max_length=400)
    title = models.CharField(max_length=244, null=True, blank=True)
    rent = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    status = models.SmallIntegerField(null=True, default=0, blank=True)
    created = models.DateField(null=True, default=timezone.now, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    description_2 = models.CharField(max_length=500, null=True, blank=True)
    subtitle = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.title}: {self.url}'

class Photo(models.Model):
    url = models.CharField(max_length=400)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.url

class Listing(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=2000)
    limit = models.IntegerField(null=True, default=0)
    post_link_list_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    post_container_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    title_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    rent_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    contact_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    description_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    picture_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    description_2_selector = models.CharField(max_length=255, default='', null=True, blank=True)
    subtitle_selector = models.CharField(max_length=255, default='', null=True, blank=True)

    def __str__(self):
        return f' {self.name}'