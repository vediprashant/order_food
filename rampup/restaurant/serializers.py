from rest_framework import exceptions, serializers

from accounts.models import User
from restaurant.models import Order, OrderedItem, ResFoodItem, Restaurant


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
    name = serializers.CharField(max_length=100, source='food_id.name')
    class Meta:
        model = OrderedItem
        fields = ['food_id', 'quantity', 'name']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializers to handle all the orders
    """
    order_items = OrderedItemSerializer(many=True)
    restaurant_name = serializers.CharField(max_length=100, source='res_id.name')

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
        user.balance = user.balance - total_amount
        for item in order_items:
            OrderedItem.objects.create(food_id=item['food_id'], 
                                       order_id=instance, amount=item['food_id'].price, 
                                       quantity=item['food_id'].quantity) 

        return instance
