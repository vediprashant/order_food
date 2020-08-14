from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from rest_framework import serializers
from rest_framework import exceptions

from .models import User
from restaurant.models import Restaurant, ResFoodItem, OrderedItem, Order


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer to handle signup of a user
    """
    restaurants_owned = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'city', 'state', 'zipcode', 'balance', 'restaurants_owned')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'balance': {'read_only': True}
        }

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    It handles all the get request
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'city', 'state', 'zipcode', 'balance', 'restaurants_owned']


class LoginSerializer(serializers.Serializer):
    """
    It validates login request for a user
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        if email and password:
            user=User.objects.get(email=email)
            if user:
                if user.check_password(password):
                    data["user"] = user
                else:
                    msg = "Password does not match!"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data


class RestaurantItemSerializer(serializers.ModelSerializer):
    """
    serializer for the items in restaurants
    """
    class Meta:
        model = ResFoodItem
        fields = ['id', 'res_id', 'name', 'price', 'quantity']
        extra_kwargs = {'id': {'read_only': True}}


class RestaurantSerializer(serializers.ModelSerializer):
    """
    It deals with all the restaurants
    """
    items = RestaurantItemSerializer(many=True, read_only='True')

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'location', 'items', 'owner_ids']
        extra_kwargs = {'id': {'read_only': True}}


class OrderedItemSerializer(serializers.ModelSerializer):
    """
    Items that were present in an order
    """

    class Meta:
        model = OrderedItem
        fields = ['food_id', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializers to handle all the orders
    """
    order_items = OrderedItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = ('status',)
        read_only_fields = ('amount',)
    """
    method to create order object and run some validations
    """
    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        user = validated_data['user_id']
        total_amount = 0
        fix_res_id = order_items[0]['food_id'].res_id

        for item in order_items:
            if item['food_id'].res_id != fix_res_id:
                raise Exception("Choose items from a single restaurant!")
            if item['food_id'].quantity < item['quantity']:
                raise Exception("Desired quantity is not available")
            total_amount += item['quantity']*(item['food_id'].price)


        if total_amount > user.balance:
            raise Exception("Balance not available, add more balance!")

        validated_data['amount'] = total_amount
        instance = Order.objects.create(**validated_data)
        for item in order_items:
            ordered_item = OrderedItem.objects.create(food_id=item['food_id'], order_id =instance, amount=item['food_id'].price, quantity=item['food_id'].quantity)
            ordered_item.save()
    
        return instance
