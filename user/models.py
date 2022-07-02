from django.db import models
import jwt
import datetime
from django.db import models
from base.models import BaseDateTime
from base.api.messages import (
    MSG_AUTH_TOKEN_INVALID,
    MSG_AUTH_TOKEN_EXPIRED,
    MSG_AUTH_TOKEN_BLACKLISTED,
)
from base.api.exceptions import PermissionDeniedException, BadRequestException
from user.choices import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, ROLE_USER, CLIENT
from django.conf import settings
from base.utils import get_access_token
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.


class User(BaseDateTime):

    username = models.CharField(
        unique=True, max_length=255, verbose_name="User Name")
    password = models.CharField(max_length=255, verbose_name="Password")
    last_login = models.DateTimeField(
        null=True, blank=True, verbose_name="Last Login")
    role = models.CharField(choices=ROLE_USER, default=CLIENT, max_length=10)

    def __str__(self):
        return self.username

    class Meta:
        db_table = "d_user"
        verbose_name = "User"

    @classmethod
    def encode_token_by_type(cls, sub, iat, exp, token_type=ACCESS_TOKEN_TYPE):
        payload = {
            "sub": sub,
            "iat": iat,
            "exp": exp,
            "type": token_type,
            "model": cls.__name__,
        }
        return jwt.encode(
            payload=payload,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    def decode_access_token(cls, auth_token, token_type=ACCESS_TOKEN_TYPE):
        try:
            payload = jwt.decode(auth_token, settings.JWT_SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise BadRequestException(message=MSG_AUTH_TOKEN_EXPIRED[1])
        except jwt.InvalidTokenError:
            raise BadRequestException(message=MSG_AUTH_TOKEN_INVALID[1])
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            raise BadRequestException(message=MSG_AUTH_TOKEN_BLACKLISTED[1])
        if payload["type"] != token_type:
            raise BadRequestException(message=MSG_AUTH_TOKEN_INVALID[1])
        return payload

    def create_access_and_refresh_token(self):
        iat = datetime.datetime.utcnow()
        exp_access_token = datetime.datetime.utcnow() + datetime.timedelta(
            days=settings.JWT_DAYS_DELTA, seconds=settings.JWT_SECONDS_DELTA
        )
        exp_refresh_token = datetime.datetime.utcnow() + datetime.timedelta(
            days=settings.JWT_DAYS_REFRESH_DELTA,
            seconds=settings.JWT_SECONDS_REFRESH_DELTA,
        )
        access_token = self.encode_token_by_type(
            self.id, iat, exp_access_token, ACCESS_TOKEN_TYPE
        )
        refresh_token = self.encode_token_by_type(
            self.id, iat, exp_refresh_token, REFRESH_TOKEN_TYPE
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    @classmethod
    def decode_auth_token(cls, auth_token, token_type=ACCESS_TOKEN_TYPE):
        payload = cls.decode_access_token(auth_token, token_type)
        if payload["model"] != cls.__name__:
            raise BadRequestException(message=MSG_AUTH_TOKEN_INVALID[1])
        return payload

    @classmethod
    def get_user_id(cls, request):
        try:
            access_token = get_access_token(request)
            payload = cls.decode_access_token(access_token)
        except Exception as ex:
            return None
        return payload["sub"]

    @classmethod
    def get_or_error_user_id(cls, request):
        try:
            access_token = get_access_token(request)
            user = cls.decode_auth_token(access_token)
        except Exception as ex:
            raise PermissionDeniedException
        return user["sub"]

    @classmethod
    def is_authenticated(self):
        return True

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "last_login": self.last_login if self.last_login else None,
        }

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class BlacklistToken(models.Model):
    user_id = models.PositiveIntegerField()
    iat = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def check_blacklist(auth_token):
        try:
            payload = jwt.decode(auth_token, settings.JWT_SECRET_KEY)
            token = BlacklistToken.objects.filter(
                user_id=payload.get("sub"),
                iat=payload.get("iat"),
                model=payload.get("model"),
            ).first()
            return bool(token)
        except jwt.ExpiredSignatureError:
            return True

    @staticmethod
    def save_token(auth_token):
        try:
            payload = jwt.decode(auth_token, settings.JWT_SECRET_KEY)
            return BlacklistToken.objects.create(
                user_id=payload.get("sub"),
                iat=payload.get("iat"),
                model=payload.get("model"),
            )
        except jwt.ExpiredSignatureError:
            pass

    class Meta:
        db_table = "d_blacklist_token"
        verbose_name = "Blacklist Token"
        verbose_name_plural = "Blacklist Token"
        indexes = [
            models.Index(fields=["user_id", "iat", "model"]),
        ]

    def __str__(self):
        return self.user_id
