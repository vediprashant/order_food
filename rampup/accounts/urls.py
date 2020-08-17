from rest_framework import routers

from django.conf.urls import url, include

from accounts import views as accounts_views 

accounts_router = routers.DefaultRouter()
accounts_router.register(r'users', accounts_views.UserViewSet, basename='users')

urlpatterns = accounts_router.urls

urlpatterns += [
    url(r'^login/', accounts_views.LoginView.as_view()),
    url(r'^logout/', accounts_views.LogoutView.as_view()),
]
