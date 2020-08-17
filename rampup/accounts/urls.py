from rest_framework import routers

from django.conf.urls import url, include

from accounts.views import LoginView, LogoutView, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^login/', LoginView.as_view()),
    url(r'^logout/', LogoutView.as_view()),
]

    