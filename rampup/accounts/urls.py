from rest_framework import routers

from django.conf.urls import url, include

from accounts.views import LoginView, LogoutView, UserViewSet

accounts_router = routers.DefaultRouter()
accounts_router.register(r'users', UserViewSet, basename='users')

urlpatterns = accounts_router.urls

urlpatterns += [
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
]

