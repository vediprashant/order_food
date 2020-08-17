from rest_framework import filters, permissions, viewsets 
from rest_framework.authentication import exceptions, TokenAuthentication
from rest_framework.request import Request
from rest_framework.response import Response

from restaurant.models import Restaurant, ResFoodItem, Order
from restaurant.permissions import IsRestaurantOwner
from restaurant.serializers import (
    OrderSerializer, RestaurantItemSerializer, RestaurantSerializer
)


class RestaurantViewSet(viewsets.ModelViewSet):
    """ 
    To handles CRUD operation on resturants
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer  


class RestaurantItemViewSet(viewsets.ModelViewSet):
    """
    To handle items present in a restaurant
    """
    serializer_class = RestaurantItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsRestaurantOwner]
        
    def get_queryset(self):
        given_id = self.request.query_params.get('id')
        queryset = ResFoodItem.objects.filter(res_id=given_id)
        return queryset


class OrderViewSet(viewsets.ModelViewSet):
      
    """
    To handle the orders
    """
    permission_classes = [permissions.IsAuthenticated]
    
    queryset = Order.objects.all()
    serializer_class = OrderSerializer   
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['res_id__name', 'order_items__food_id__name']
    def get_queryset(self):
        queryset = Order.objects.filter(user_id=self.request.user).order_by('res_id__name', 'amount')
        return queryset
