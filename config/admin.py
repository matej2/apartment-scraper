from django.contrib import admin

# Register your models here.
from config.models import Webhook


class WebhookAdmin(admin.ModelAdmin):
    list_display = ("name",)
    save_as = True

admin.site.register(Webhook, WebhookAdmin)
