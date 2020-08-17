from rest_framework import permissions, exceptions

from restaurant.models import Restaurant

class IsRestaurantOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        given_id = request.query_params.get('id')
        if given_id is None:
            raise exceptions.AuthenticationFailed("provide restaurant id with id as a parameter")
        restaurant_object = Restaurant.objects.get(pk=given_id)
        if request.user not in restaurant_object.owner_ids.all():
            raise exceptions.AuthenticationFailed("Not an owner")
        return True
