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
        return self.title


class Listing(models.Model):
    url = models.CharField(max_length=500)
    limit = models.IntegerField(null=True, default=0)
    post_link_list_selector = models.CharField(max_length=255, default='')
    post_container_selector = models.CharField(max_length=255, default='')
    title_selector = models.CharField(max_length=255, default='')
    rent_selector = models.CharField(max_length=255, default='')
    contact_selector = models.CharField(max_length=255, default='')
    desc_selector = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.url


class Parameter(models.Model):
    name = models.CharField(max_length=255, default='')
    selector = models.CharField(max_length=255, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class ApartmentParameter(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    value = models.CharField(max_length=500, null=True)
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.apartment.title) + " - " + str(self.parameter.name)
