from django.contrib import admin

from restaurant import models as restaurant_models

admin.site.register(restaurant_models.Restaurant)
admin.site.register(restaurant_models.ResFoodItem)
admin.site.register(restaurant_models.Order)
admin.site.register(restaurant_models.OrderedItem)
