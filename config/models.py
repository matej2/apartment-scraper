from django.db import models

# Create your models here.
from scraper.models import Listing


class Webhook(models.Model):
    url = models.CharField(max_length=400)
    name = models.CharField(max_length=244, null=True)

    def __str__(self):
        return self.name

class WebhookListing(models.Model):
    listing = models.ForeignKey(Webhook, on_delete=models.CASCADE, blank=True, null=True)
    webhook = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.webhook.name} - {self.listing}'
