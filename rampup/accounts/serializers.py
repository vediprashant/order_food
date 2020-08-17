from rest_framework import serializers
from rest_framework import exceptions

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from .models import User
from restaurant.models import Order, OrderedItem, ResFoodItem, Restaurant


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer to handle signup of a user
    """
    restaurants_owned = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'city', 'state', 'zipcode', 'balance', 'restaurants_owned')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'balance': {'read_only': True}
        }

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    It handles all the get request
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'city', 'state', 'zipcode', 'balance', 'restaurants_owned']


class LoginSerializer(serializers.Serializer):
    """
    It validates login request for a user
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user=User.objects.filter(email=email)
            if user:
                if user.check_password(password):
                    data["user"] = user
                else:
                    msg = "Password does not match!"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise exceptions.ValidationError(msg)
        return data
