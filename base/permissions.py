from rest_framework.permissions import BasePermission, AllowAny
from base.middleware import GlobalRequestMiddleware
from base.utils import get_access_token, check_client_key
from user.models import User
from user.choices import CLIENT, MANAGER, EMPLOYEE
from base.choices import SAFE_METHOD_CLIENT, SAFE_METHOD_MANAGER, SAFE_METHOD_EMPLOYEE


class IsAppVerified(AllowAny):
    """
    verify client api key
    """

    message = {"code": 403, "message": "You don't have permission to access api"}

    def has_permission(self, request, view):
        return check_client_key(request)


def request_to_auth_info(request, cls_auth=None):
    try:
        if hasattr(request, "user_id") and request.user_id and request.role:
            return {
                "user_id": request.user_id,
                "user": request.user,
                "role": request.role
            }
        if not cls_auth:
            payload = User.decode_access_token(get_access_token(request))
        else:
            payload = cls_auth.decode_auth_token(get_access_token(request))

        user = User.objects.get(pk=payload["sub"])

        result = {
            "user_id": payload["sub"],
            "user": user,
            "role": user.role
        }

        # set other value for request
        request.user_id = result["user_id"]
        request.user = result["user"]
        request.role = result["role"]

        # set request with new value
        GlobalRequestMiddleware.GLOBAL_REQUEST_STORAGE.request = request
        return result
    except:
        return None


class Authentication(BasePermission):
    message = {"code": 401, "message": "Invalid token. Please log in again."}
    cls_auth = None

    def has_object_permission(self, request, view, obj):
        return True


class ClientAuthOnlyCreate(Authentication):

    def has_permission(self, request, view):
        request_auth = request_to_auth_info(
            request=request, cls_auth=self.cls_auth)
        print(request_auth)
        print(request.method)
        if not request_auth or request_auth.get("role") != CLIENT or request.method not in SAFE_METHOD_CLIENT:
            return False
        return True


class ManagerAuthDeleteAssign(Authentication):
    method_message = 'User need permisison to use api'

    def has_permission(self, request, view):
        request_auth = request_to_auth_info(
            request=request, cls_auth=self.cls_auth)
        print(request_auth)
        print(request.method)
        if not request_auth or request_auth.get("role") != MANAGER or request.method not in SAFE_METHOD_EMPLOYEE:
            return False
        return True


class EmployeeAuthDeleteComplete(Authentication):
    method_message = 'User need permisison to use api'

    def has_permission(self, request, view):
        request_auth = request_to_auth_info(
            request=request, cls_auth=self.cls_auth)
        print(request_auth)
        print(request.method)
        if not request_auth or request_auth.get("role") != EMPLOYEE or request.method not in SAFE_METHOD_EMPLOYEE:
            return False
        return True
