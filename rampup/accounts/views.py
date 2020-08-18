from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    exceptions, get_authorization_header, TokenAuthentication
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from accounts import (
    models as accounts_models, permissions as accounts_permissions,
    serializers as accounts_serializers,
)



class UserViewSet(viewsets.ModelViewSet):
    """
    View to handle all the request to user
    """
    # Adds permission classes based on the request
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = []
        elif self.action == 'list':
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticated, accounts_permissions.IsOwner]
        return super(UserViewSet, self).get_permissions()
 
    queryset = accounts_models.User.objects.all()

    #Redirect towards the required serializer based on request
    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PUT':
            return accounts_serializers.RegisterSerializer
        else:
            return accounts_serializers.UserSerializer
    

class LoginView(GenericAPIView):
    """
    It log's in a user and add a token
    """
    serializer_class = accounts_serializers.LoginSerializer
    
    def post(self, request):
        serializer = accounts_serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "user": self.serializer_class(user, context=self.get_serializer_context()).data,
            "token": token.key
            })


class LogoutView(APIView):
    """
    It deletes the token and logout user
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = [permissions.IsAuthenticated]
   
    def post(self, request):
    
        token_object = Token.objects.filter(user=request.user)
        token_object.delete()
        return Response(status=204)
