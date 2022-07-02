from datetime import datetime
from rest_framework.views import APIView
from base.api.mixins import CreateModelMixin
from rest_framework import generics
from user.models import User
from user.api.serializers import SignUpSerializer, LoginSerializer
from base.api.messages import MSG_CREATE_SUCCESS_USER
from base.api.response import SuccessResponse, ValidationErrorResponse
from base.api.exceptions import NotFoundException
from django.contrib.auth.hashers import check_password, make_password


class RegisterView(CreateModelMixin, generics.CreateAPIView):

    success_response = MSG_CREATE_SUCCESS_USER
    serializer_class = SignUpSerializer

    def get_success_response(self, serializer):
        return SuccessResponse(
            data=serializer.instance.to_json(),
            status=self.status_code,
            code=self.success_response[0],
            message=self.success_response[1],
        )

    def get_credentials(self, request):
        data = request.data
        data["last_login"] = datetime.now()
        return data


class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        credentials = self.get_credentials()
        serializer = LoginSerializer(data=credentials)
        if not serializer.is_valid():
            pass
        instance = self.get_object(credentials)
        if instance and instance.password and check_password(credentials.get("password"), instance.password):
            return SuccessResponse(data=instance.create_access_and_refresh_token())
        return ValidationErrorResponse(message="Username or Password is not correct")

    def get_credentials(self):
        return self.request.data

    def get_object(self, credentials):
        try:
            return User.objects.get(username=credentials.get("username"))
        except User.DoesNotExist as ex:
            raise NotFoundException(message="User not found")
