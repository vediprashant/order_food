from rest_framework import routers

from django.conf.urls import url, include

from restaurant import views as restaurant_views

restaurant_router = routers.DefaultRouter()
restaurant_router.register(r'restaurant', restaurant_views.RestaurantViewSet)
restaurant_router.register(r'item', restaurant_views.RestaurantItemViewSet, basename='ResFoodItem')
restaurant_router.register(r'order', restaurant_views.OrderViewSet, basename='Order')
restaurant_router.register(r'reports', restaurant_views.UsersOrderedViewSet, basename='Order')
