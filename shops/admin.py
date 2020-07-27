from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Shop,Order,Type,Profile

@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    list_display = ('name', 'location')

admin.site.register(Order)
admin.site.register(Type)
admin.site.register(Profile)