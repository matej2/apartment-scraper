from django.contrib import admin

# Register your models here.
from scraper.models import Apartment, Listing, ApartmentParameter, Parameter


class ApartmentAdmin(admin.ModelAdmin):
    list_display = ("url", "title", "rent", "contact")


class ListingAdmin(admin.ModelAdmin):
    list_display = ("url", "limit", "post_link_list_selector", "post_container_selector", "title_selector", "rent_selector", "contact_selector")

class ApartmentParameterAdmin(admin.ModelAdmin):
    list_display = ("apartment", "parameter", "value")

class ParameterAdmin(admin.ModelAdmin):
    list_display = ("name", "selector", "listing")


admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(ApartmentParameter, ApartmentParameterAdmin)
admin.site.register(Parameter, ParameterAdmin)
