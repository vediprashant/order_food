from rest_framework import permissions, exceptions

from restaurant import models as restaurant_models

class IsRestaurantOwner(permissions.BasePermission):
    """
    To determine the is user is the owner of restaurant
    """
    def has_permission(self, request, view):
        given_id = request.query_params.get('id')
        if given_id is None:
            raise exceptions.AuthenticationFailed("provide restaurant id with id as a parameter")
        restaurant_object = restaurant_models.Restaurant.objects.get(pk=given_id)
        if request.user not in restaurant_object.owners.all():
            raise exceptions.AuthenticationFailed("Not an owner")
        return True
