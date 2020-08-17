from rest_framework import routers

from django.conf.urls import url, include

from accounts.views import UserViewSet

accounts_router = routers.DefaultRouter()
accounts_router.register(r'users', UserViewSet, basename='users')

