from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view and edit it.
    """

    def has_object_permission(self, request, view, obj):
        #check whether the user is the owner of the data
        return obj == request.user
        