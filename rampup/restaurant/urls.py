from rest_framework import routers

from django.conf.urls import url, include

from restaurant.views import RestaurantViewSet, RestaurantItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'restaurant', RestaurantViewSet)
router.register(r'item', RestaurantItemViewSet, basename='ResFoodItem')
router.register(r'order', OrderViewSet, basename='Order')
