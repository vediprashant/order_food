from rest_framework import filters, permissions, viewsets 
from rest_framework.authentication import exceptions, TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response

from restaurant import (
    models as restaurant_models, 
    permissions as restaurant_permissions,
    serializers as restaurant_serializers,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """ 
    To handles CRUD operation on resturants
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = restaurant_models.Restaurant.objects.all()
    serializer_class = restaurant_serializers.RestaurantSerializer  


class RestaurantItemViewSet(viewsets.ModelViewSet):
    """
    To handle items present in a restaurant
    """
    serializer_class = restaurant_serializers.RestaurantItemSerializer
    permission_classes = [permissions.IsAuthenticated, restaurant_permissions.IsRestaurantOwner]
        
    def get_queryset(self):
        given_id = self.request.query_params.get('id')
        queryset = restaurant_models.ResFoodItem.objects.filter(restaurant=given_id)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
      
    """
    To handle the orders
    """
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = restaurant_models.Order.objects.all()
    serializer_class = restaurant_serializers.OrderSerializer   
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['restaurant__name', 'order_items__food__name']
    def get_queryset(self):
        queryset = restaurant_models.Order.objects.filter(user=self.request.user).order_by('restaurant__name', 'amount')
        return queryset


class UsersOrderedViewSet(viewsets.ModelViewSet):
    """
    To show all the users that have placed some order from restaurant
    """
    serializer_class = restaurant_serializers.UsersOrderedSerializer
    
    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated]
        given_id = self.request.query_params.get('id')
        if given_id is None:
            raise exceptions.AuthenticationFailed("provide restaurant id with id as a parameter")
        restaurant_object = restaurant_models.Restaurant.objects.get(pk=given_id)
        if self.request.user not in restaurant_object.owner_ids.all():
            raise exceptions.AuthenticationFailed("Not an owner")
        return super().get_permissions()

    def get_queryset(self):
        given_id = self.request.query_params.get('id')
        return restaurant_models.Order.objects.filter(res_id=given_id).distinct('user_id')

