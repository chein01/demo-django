from rest_framework import serializers
from user.models import User
from base.api.exceptions import ValidationException
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation
import re


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", "last_login", "role"]

    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return make_password(value)

    def validate_username(self, value):
        if not re.match(r'[a-zA-Z0-9@#-]+', value):
            raise ValidationException(message="Username is not valid")
        return value


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password"]
