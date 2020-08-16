
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    TokenAuthentication, get_authorization_header, exceptions
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import User
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer, 
)

class UserViewSet(viewsets.ModelViewSet):
    """
    View to handle all the request to user
    """
    """
    Adds permission classes based on the request
    """
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        else:
            self.permission_classes = [permissions.IsAuthenticated]
        return super(UserViewSet, self).get_permissions()
 
    queryset = User.objects.all()
    """
    Redirect towards the required serializer based on request
    """
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return RegisterSerializer
        else:
            return UserSerializer


class LoginView(GenericAPIView):
    """
    It log's in a user and add a token
    """
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
            })


class LogoutView(APIView):
    """
    It deletes the token and logout user
    """
    authentication_classes = (TokenAuthentication, )
   
    def post(self, request):
        auth = get_authorization_header(request).split()
        if not auth:
            raise exceptions.AuthenticationFailed('Authenticate First')
        if len(auth) == 1:
            msg = ('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = ('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = ('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)
        token_object = Token.objects.filter(key=token)
        if token_object:
            token_object.delete()
        else:
            raise exceptions.AuthenticationFailed("Given Token not associated with the user")
        return Response(status=204)
