import time
import os
import datetime
from base.choices import (
    CLIENT_LANG_KEY,
    HTTP_AUTHORIZATION,
    VERIFY_CLIENT_API_KEY,
)
from django.core.exceptions import ValidationError
from django.db.models import F
from django.conf import settings

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def base_upload(filename, path="default/file"):
    new_filename = time.time()
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "{path}/{final_filename}".format(path=path, final_filename=final_filename)


def write_error(e):
    print("--------------------------------------- Error: ")
    print(e)
    # logger.exception(e)


def format_date(date, format="%d/%m/%Y"):
    return date.strftime(format) if date else None


def format_datetime(datetime, format="%d/%m/%Y %H:%M:%S"):
    return datetime.strftime(format) if datetime else None


def get_access_token(request):
    from base.api.exceptions import BadRequestException
    from base.api.messages import MSG_AUTH_TOKEN_INVALID

    try:
        return request.META.get(HTTP_AUTHORIZATION).split(" ")[1]
    except (AttributeError, IndexError):
        raise BadRequestException(message=MSG_AUTH_TOKEN_INVALID[1])


def check_client_key(request, class_auth=None):
    if request.META.get(VERIFY_CLIENT_API_KEY) == settings.CLIENT_API_KEY:
        return True
    if class_auth:
        class_auth.message = {
            "code": 403,
            "message": "You don't have permission to access api",
        }
    return False
