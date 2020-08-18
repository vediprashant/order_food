from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.db import models

from common import (
    constants as common_constants, models as common_models,
 )


class MyUserManager(BaseUserManager):
    def create_user(self, **kwargs):
        """
        Creates and saves a user with given parameters
        """
        if not email:
            raise ValueError('user must have an email address')

        user = self.model(**kwargs)
        user.email = self.normalize_email(self.email)
        user.set_password(self.password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        """
        Creates and saves a superuser with given credentials
        """
        return self.create_user(**kwargs)


class User(AbstractBaseUser, PermissionsMixin, common_models.TimeStampModel):
    """
    Model to store the details of all the users
    """
    name = models.CharField(max_length=common_constants.MAX_NAME_LENGTH)
    email = models.EmailField(unique=True) 
    city = models.CharField(max_length=common_constants.MAX_PLACE_LENGTH)
    state = models.CharField(max_length=common_constants.MAX_PLACE_LENGTH)
    zipcode = models.CharField(max_length=common_constants.MAX_PLACE_LENGTH, blank=True)
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
        
