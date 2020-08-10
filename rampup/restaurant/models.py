from django.db import models
from There4U.models import User
class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 30)
    owners_id = models.ManyToManyField(User)


class ResFoodItem(models.Model):
    name = models.CharField(max_length = 100)
    price = models.IntegerField()
    quantity = models.IntegerField()
    res_id = models.ForeignKey(Restaurant, on_delete = models.CASCADE)


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    res_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    time = models.DateTimeField()
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
    res_food_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()
    quantity = models.IntegerField()