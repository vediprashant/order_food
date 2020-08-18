from rest_framework import exceptions, serializers

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

from accounts import models as accounts_model
from restaurant import serializers as restaurants_serializer


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer to handle signup of a user
    """
    class Meta:
        model = accounts_model.User
        fields = ('id', 'name', 'email', 'password', 'city', 'state', 'zipcode', 'balance')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8},
                        'balance': {'read_only': True},
        }

    def create(self, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterSerializer,self).update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    It handles all the get request
    """
    restaurants_owned = restaurants_serializer.RestaurantsOwnedSerializer(many=True)
    class Meta:
        model = accounts_model.User
        fields = ['name', 'email', 'city', 'state', 'zipcode', 'balance', 'restaurants_owned']
        extra_kwargs = {'restaurants_owned': {'read_only': True}}


class LoginSerializer(serializers.Serializer):
    """
    It validates login request for a user
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = accounts_model.User.objects.filter(email=email).first()
        if user and user.check_password(password):
            data["user"] = user
        else:
            msg = "Unable to login with given credentials."
            raise exceptions.ValidationError(msg)
        
        return data
