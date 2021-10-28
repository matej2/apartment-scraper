from django.db import models

# Create your models here.


class Webhook(models.Model):
    url = models.CharField(max_length=400)
    name = models.CharField(max_length=244, null=True)

    def __str__(self):
        return self.name

