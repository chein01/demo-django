from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from user.api.views import  RegisterView, LoginView

urlpatterns = [

    path("register", RegisterView.as_view(), name="Register User By Username, Password"),
    path("login", LoginView.as_view(), name="Login By Password"),

]

urlpatterns = format_suffix_patterns(urlpatterns)
