from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class MyUserManager(BaseUserManager):
    def create_user(self, name, email, city, state, zipcode):
        """
        Creates and saves a user with given parameters
        """
        if not email:
            raise ValueError('user must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            name = name,
            city = city,
            state = state,
            zipcode = zipcode,
            balance = 1000
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    balance = models.IntegerField(default=1000)
    username = None
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    REQUIRED_FIELDS = ['name', 'city', 'state', 'zipcode']
