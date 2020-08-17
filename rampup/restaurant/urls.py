from rest_framework import routers

from django.conf.urls import url, include

from restaurant.views import RestaurantViewSet, RestaurantItemViewSet, OrderViewSet

restaurant_router = routers.DefaultRouter()
restaurant_router.register(r'restaurant', RestaurantViewSet)
restaurant_router.register(r'item', RestaurantItemViewSet, basename='ResFoodItem')
restaurant_router.register(r'order', OrderViewSet, basename='Order')
