from django.contrib import admin

# Register your models here.
from config.models import Webhook, WebhookListing


class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name",)
    save_as = True

class WebhookListingAdmin(admin.ModelAdmin):
    list_display = ("webhook", "listing")
    save_as = True


admin.site.register(Webhook, WebhookAdmin)
admin.site.register(WebhookListing, WebhookListingAdmin)