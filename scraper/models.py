from django.db import models

# Create your models here.


class Apartment(models.Model):
    url = models.CharField()
    title = models.CharField()
    rent = models.IntegerField()
    contact = models.CharField()

    def __str__(self):
        return self.title + ": " + self.contact
