from django.utils.translation import gettext_lazy as __

MSG_SUCCESS = (200, __("Succeed"))
MSG_CREATE_SUCCESS = (201, __("Create success"))
MSG_DESTROY_SUCCESS = (201, __("Destroy success"))
MSG_AUTH_TOKEN_INVALID = (400, __("Invalid token. Please log in again."))
MSG_AUTH_TOKEN_EXPIRED = (401, __("Signature expired. Please log in again."))
MSG_AUTH_TOKEN_BLACKLISTED = (402, __("Token blacklisted. Please log in again."))
MSG_AUTH_NOT_ALLOWED = (403, __("You do not have permission to perform this action."))
MSG_CREATE_SUCCESS_USER = (201, __("Create User Success"))


# app auth permission
