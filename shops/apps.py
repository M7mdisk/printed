from django.apps import AppConfig


class ShopsConfig(AppConfig):
    name = 'shops'
    #label = "shop.conf"
    def ready(self):
    	import shops.signals