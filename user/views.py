from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions, renderers, viewsets, status, generics
from django.http import JsonResponse
from rest_framework.exceptions import APIException
from .models import *
from .serializers import *
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from dj_rest_auth.serializers import PasswordResetSerializer
import datetime
from django.conf import settings
import json
import requests
from django.http import JsonResponse
import traceback
import pyotp
import logging


logger = logging.getLogger(__name__)


class CustomAuthToken(ObtainAuthToken):
    """Get a user Token"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email,
            'username': user.username,
        })


class CustomLoginView(LoginView):
    """
    Login Route
    """

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.data,
                                              context={'request': request})
        if not self.serializer.is_valid():
            return Response({'message': 'username or password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            #self.serializer.is_valid(raise_exception=True)

            self.login()
            return self.get_response()

    def get_response(self):
        orginal_response = super().get_response()
        username = self.request.user
        user = authenticate(username=username,
                            password=self.request.data['password'])
        #user = User.objects.get(username__iexact=username)
        #username__iexact=username
        email = user.email
        name = user.username
        is_creator = user.is_creator
        token = Token.objects.get(user=user)
        datum = {"token": token.key, "id": user.id,
                 "username": name, "email": email}
        #print(datum)
        #mydata = {"message": "some message", "status": "success"}
        orginal_response.data.update(datum)
        return orginal_response
      
      
class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_update(self, serializer):
        try:
          serializer.save()
        except Exception as e:
            print(str(e))
            traceback.print_exc()
            return Response(data={'message': str(e)})
