from datetime import datetime

from django.db import models

from accounts import models as accounts_models
from common import (
    constants as common_constants, models as common_models
)


class Restaurant(common_models.TimeStampModel):
    """
    Model having details of the restaurants
    """
    name = models.CharField(max_length=common_constants.MAX_NAME_LENGTH)
    location = models.CharField(max_length=common_constants.MAX_NAME_LENGTH)
    owners = models.ManyToManyField(accounts_models.User, related_name='restaurants_owned')

    def __str__(self):
        return self.name


class ResFoodItem(common_models.TimeStampModel):
    """
    Model which represent the items that are present in restaurants
    """
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name="items")
    name = models.CharField(max_length=common_constants.MAX_NAME_LENGTH)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name


class Order(common_models.TimeStampModel):
    """
    Model to store the deatils of the orders placed by users
    """
    user = models.ForeignKey(accounts_models.User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=common_constants.STATUS_CHOICES, default=common_constants.PLACED)

    def __str__(self):
        return f"{self.restaurant.name} {self.amount}"


class OrderedItem(common_models.TimeStampModel):
    """
    Model to store the items that were present in an order
    """
    food = models.ForeignKey(ResFoodItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    amount = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.food.name)
