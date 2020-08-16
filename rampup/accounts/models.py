from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **kwargs):
        """
        Creates and saves a user with given parameters
        """
        if not email:
            raise ValueError('user must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password, **kwargs):
        """
        Creates and saves a superuser with given credentials
        """
        user = self.create_user(email,
            name=name,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Model to store the details of all the users
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    zipcode = models.CharField(max_length=30, null=True)
    balance = models.PositiveIntegerField(default=1000)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

   
    USERNAME_FIELD = 'email'

    objects = MyUserManager()

    REQUIRED_FIELDS = ['name']

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email
        