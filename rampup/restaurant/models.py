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

    def __str__(self):
        return self.name


class ResFoodItem(models.Model):
    """
    Model which represent the items that are present in restaurants
    """
    res_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name="items")
    name = models.CharField(max_length = 100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Model to store the deatils of the orders placed by users
    """
    PLACED = 'placed'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    DISPATCHED = 'dispatched'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PLACED, 'placed'),
        (ACCEPTED, 'accepted'),
        (REJECTED, 'rejected'),
        (DISPATCHED, 'dispatched'),
        (DELIVERED, 'delivered'),
        (CANCELLED, 'cancelled')
    ]
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
   
    status = models.CharField(max_length=10, choices = STATUS_CHOICES, default = PLACED)

    def __str__(self):
        return self.status


class OrderedItem(models.Model):
    """
    Model to store the items that were present in an order
    """
    food_id = models.ForeignKey(ResFoodItem, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
