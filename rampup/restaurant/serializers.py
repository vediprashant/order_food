from rest_framework import exceptions, serializers

from accounts import models as accounts_models
from restaurant import models as restaurant_models


class RestaurantItemSerializer(serializers.ModelSerializer):
    """
    serializer for the items in restaurants
    """
    class Meta:
        model = restaurant_models.ResFoodItem
        fields = ['id', 'restaurant', 'name', 'price', 'quantity']
        extra_kwargs = {'id': {'read_only': True}}


class RestaurantSerializer(serializers.ModelSerializer):
    """
    It deals with all the restaurants
    """
    items = RestaurantItemSerializer(many=True, read_only='True')

    class Meta:
        model = restaurant_models.Restaurant
        fields = ['id', 'name', 'location', 'items', 'owners']
        extra_kwargs = {'id': {'read_only': True}}


class OrderedItemSerializer(serializers.ModelSerializer):
    """
    Items that were present in an order
    """
    name = serializers.CharField(max_length=30, source='food.name', read_only=True)
    class Meta:
        model = restaurant_models.OrderedItem
        fields = ['food', 'quantity', 'name']
        extra_kwargs = {'food': {'write_only': True}}


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializers to handle all the orders
    """
    order_items = OrderedItemSerializer(many=True)
    restaurant_name = serializers.CharField(max_length=30, source='restaurant.name', read_only=True)

    class Meta:
        model = restaurant_models.Order
        fields = ['order_items', 'user', 'restaurant','amount', 'status', 'restaurant_name']
        extra_kwargs = {'user': {'read_only': True},
                        'restaurant': {'write_only': True},
                        'amount': {'read_only': True},
                        'status': {'read_only': True},
        }
    
    # method to create order object and run some validations
    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        user = self.context['request'].user
        total_amount = 0
        fix_res_id = order_items[0]['food'].restaurant

        for item in order_items:
            if item['food'].restaurant != fix_res_id:
                raise Exception("Choose items from a single restaurant!")
            if item['food'].quantity < item['quantity']:
                raise Exception("Desired quantity is not available")
            total_amount += item['quantity']*(item['food'].price)


        if total_amount > user.balance:
            raise Exception("Balance not available, add more balance!")

        validated_data['amount'] = total_amount
        validated_data['user'] = user
        instance = restaurant_models.Order.objects.create(**validated_data)
        user.balance = user.balance - total_amount
        user.save()
        for item in order_items:
            restaurant_models.OrderedItem.objects.create(food=item['food'], 
                                       order=instance, amount=item['food'].price, 
                                       quantity=item['quantity']) 

        return instance


class UsersOrderedSerializer(serializers.ModelSerializer):
    """
    serializer to show users that ordered from a restaurant
    """
    user = serializers.CharField(max_length=30, source='user.email')
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
