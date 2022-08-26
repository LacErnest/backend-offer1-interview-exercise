from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse

from .models import User
from datetime import date, datetime as dt
from offer1_backend.mixins.get_or_none import get_or_none
from rest_framework.authtoken.models import Token


class TokenSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_email(self, obj):
        return obj.user.email

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Token
        fields = ('key', 'user', 'email', 'username')


class UserSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', ]


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'username')

    def get_cleaned_data(self):
        return{
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        try:
            adapter = get_adapter()
            user = adapter.new_user(request)
            self.cleaned_data = self.get_cleaned_data()
            email = self.cleaned_data.get('email')
            user.first_name = self.cleaned_data.get('first_name')
            user.last_name = self.cleaned_data.get('last_name')
            user_email = User.objects.filter(email=email)
            if user_email.exists():
                return JsonResponse({"error": True, "message": "email already in use"})
            user.save()
            adapter.save_user(request, user, self)
            return user
        except Exception as e:
            return JsonResponse({"error": True, "message": str(e)})
