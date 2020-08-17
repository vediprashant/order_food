from rest_framework import exceptions, serializers

from accounts.models import User
from restaurant import models as restaurant_models


class RestaurantItemSerializer(serializers.ModelSerializer):
    """
    serializer for the items in restaurants
    """
    class Meta:
        model = restaurant_models.ResFoodItem
        fields = ['id', 'res_id', 'name', 'price', 'quantity']
        extra_kwargs = {'id': {'read_only': True}}


class RestaurantSerializer(serializers.ModelSerializer):
    """
    It deals with all the restaurants
    """
    items = RestaurantItemSerializer(many=True, read_only='True')

    class Meta:
        model = restaurant_models.Restaurant
        fields = ['id', 'name', 'location', 'items', 'owner_ids']
        extra_kwargs = {'id': {'read_only': True}}


class OrderedItemSerializer(serializers.ModelSerializer):
    """
    Items that were present in an order
    """
    name = serializers.CharField(max_length=30, source='food_id.name')
    class Meta:
        model = restaurant_models.OrderedItem
        fields = ['food_id', 'quantity', 'name']
        extra_kwargs = {'name': {'read_only': True},
                        'food_id': {'write_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializers to handle all the orders
    """
    order_items = OrderedItemSerializer(many=True)
    restaurant_name = serializers.CharField(max_length=30, source='res_id.name')

    class Meta:
        model = restaurant_models.Order
        fields = ['order_items', 'user_id', 'res_id','amount', 'status', 'restaurant_name']
        extra_kwargs = {'user_id': {'read_only': True},
                        'res_id': {'write_only': True},
                        'amount': {'read_only': True},
                        'status': {'read_only': True},
                        'restaurant_name': {'read_only': True}
        }
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
        instance = restaurant_models.Order.objects.create(**validated_data)
        user.balance = user.balance - total_amount
        for item in order_items:
            restaurant_models.OrderedItem.objects.create(food_id=item['food_id'], 
                                       order_id=instance, amount=item['food_id'].price, 
                                       quantity=item['food_id'].quantity) 

        return instance


class UsersOrderedSerializer(serializers.ModelSerializer):
    """
    serializer to show users that ordered from a restaurant
    """
    user = serializers.CharField(max_length=30, source='user_id.email')
    class Meta:
        model = restaurant_models.Order
        fields = ['user', ]

class RestaurantsOwnedSerializer(serializers.ModelSerializer):
    """
    Serializer to show owners
    """
    class Meta:
        model = restaurant_models.Restaurant
        fields = ['name']