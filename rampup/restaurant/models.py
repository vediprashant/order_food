from django.db import models
from accounts.models import User

from datetime import datetime

class Restaurant(models.Model):
    """
    Model having details of the restaurants
    """
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    owner_ids = models.ManyToManyField(User, related_name='restaurants_owned')


class ResFoodItem(models.Model):
    """
    Model which represent the items that are present in restaurants
    """
    name = models.CharField(max_length = 100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    res_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE)


class Order(models.Model):
    """
    Model to store the deatils of the orders placed by users
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    status_choices = [
        ('placed', 'placed'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
        ('dispatched', 'dispatched'),
        ('delivered', 'delivered'),
        ('cancelled', 'cancelled')
    ]
    status = models.CharField(max_length=10, choices = status_choices, default = 'placed')


class Ordered_Item(models.Model):
    """
    Model to store the items that were present in an order
    """
    res_food_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField()
