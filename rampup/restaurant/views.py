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
    # search_fields = ['restaurant_name', 'order_items.name', 'amount']
    # ordering = ['restaurant_name', 'amount']
    def list(self, request):
        queryset = Order.objects.filter(user_id=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
