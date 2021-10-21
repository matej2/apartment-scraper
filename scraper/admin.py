from django.contrib import admin

# Register your models here.
from scraper.models import Apartment, Listing, Photo


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "rent", "contact")
    save_as = True


class ListingAdmin(admin.ModelAdmin):
    list_display = ("url", "limit", "post_link_list_selector", "post_container_selector", "title_selector", "rent_selector", "contact_selector", "description_selector")
    save_as = True

class PhotoAdmin(admin.ModelAdmin):
    list_display = ("url", "apartment")
    save_as = True


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Photo, PhotoAdmin)