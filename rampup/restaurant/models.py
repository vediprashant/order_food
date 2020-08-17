from datetime import datetime

from django.db import models

from accounts.models import User
from common.constants import max_name_length, max_place_length, PLACED, STATUS_CHOICES
from common.models import TimeStampModel


class Restaurant(TimeStampModel):
    """
    Model having details of the restaurants
    """
    name = models.CharField(max_length=max_name_length)
    location = models.CharField(max_length=max_name_length)
    owner_ids = models.ManyToManyField(User, related_name='restaurants_owned')

    def __str__(self):
        return self.name


class ResFoodItem(TimeStampModel):
    """
    Model which represent the items that are present in restaurants
    """
    res_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name="items")
    name = models.CharField(max_length=max_name_length)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Order(TimeStampModel):
    """
    Model to store the deatils of the orders placed by users
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PLACED)

    def __str__(self):
        return str(self.res_id.name) + " " + str(self.amount)


class OrderedItem(TimeStampModel):
    """
    Model to store the items that were present in an order
    """
    food_id = models.ForeignKey(ResFoodItem, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.food_id.name)
