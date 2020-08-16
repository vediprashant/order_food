from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, exceptions
from rest_framework.request import Request
from rest_framework.response import Response

from restaurant.models import Restaurant, ResFoodItem, Order
from .serializers import (
    RestaurantSerializer, RestaurantItemSerializer, OrderSerializer
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
    
    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated]
        given_id = self.request.query_params.get('id')
        if given_id is None:
            raise exceptions.AuthenticationFailed("provide restaurant id with id as a parameter")
        restaurant_object = Restaurant.objects.get(pk=given_id)
        if self.request.user not in restaurant_object.owner_ids.all():
            raise exceptions.AuthenticationFailed("Not an owner")
        return super().get_permissions()
        
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
    def list(self, request):
        queryset = Order.objects.filter(user_id=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
