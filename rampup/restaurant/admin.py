from django.contrib import admin

from .models import Restaurant, ResFoodItem, Order, Ordered_Item

admin.site.register(Restaurant)
admin.site.register(ResFoodItem)
admin.site.register(Order)
admin.site.register(Ordered_Item)
