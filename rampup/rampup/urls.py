"""rampup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from accounts.views import LoginView, LogoutView, UserViewSet
from restaurant.views import RestaurantViewSet, RestaurantItemViewSet, OrderViewSet
from django.contrib import admin 


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'restaurant', RestaurantViewSet)
router.register(r'item', RestaurantItemViewSet, basename='ResFoodItem')
router.register(r'order', OrderViewSet, basename='Order')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
]
