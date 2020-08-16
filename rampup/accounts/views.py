
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    TokenAuthentication, get_authorization_header, exceptions
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import mixins

from .models import User
from restaurant.models import Restaurant, ResFoodItem, OrderedItem, Order
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, 
    RestaurantSerializer, RestaurantItemSerializer, OrderSerializer, UsersOrderedSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    """
    View to handle all the request to user
    """
    """
    Adds permission classes based on the request
    """
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(UserViewSet, self).get_permissions()
 
    queryset = User.objects.all()
    """
    Redirect towards the required serializer based on request
    """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        else:
            return UserSerializer


class LoginView(GenericAPIView):
    """
    It log's in a user and add a token
    """
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
            })


class LogoutView(APIView):
    """
    It deletes the token and logout user
    """
    authentication_classes = (TokenAuthentication, )
   
    def post(self, request):


        auth = get_authorization_header(request).split()
        if not auth:
            raise exceptions.AuthenticationFailed('Authenticate First')
        if len(auth) == 1:
            msg = ('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = ('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        token_object = Token.objects.get(key=token)
        token_object.delete()

        return Response(status=204)


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


class UsersOrderedViewSet(viewsets.ModelViewSet):
    """
    To show all the users that have placed some order from restaurant
    """
    serializer_class = UsersOrderedSerializer
    
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
        queryset = Order.objects.filter(res_id=given_id).distinct('user_id')
        # user_queryset = queryset.objects.order_by('user_id').distinct('user_id')
        return queryset
    