from django.contrib import admin

from .models import Restaurant, ResFoodItem, Order, OrderedItem

admin.site.register(Restaurant)
admin.site.register(ResFoodItem)
admin.site.register(Order)
admin.site.register(OrderedItem)
