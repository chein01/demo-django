"""demo_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.conf import settings

urlpatterns = []
is_cms_enabled = settings.APP_MOD in (settings.APP_MOD_CMS, settings.APP_MOD_FULL)
is_api_enabled = settings.APP_MOD in (settings.APP_MOD_API, settings.APP_MOD_FULL)

cms_urls = (path("admin/", admin.site.urls),) if is_cms_enabled else []

api_urls = [
    path(
        "api/v1/",
        include(
            [
                path("users/", include("user.api.urls"), name="User"),
                path("tasks/", include("task.api.urls"), name="Task"),

            ]
        ),
        name="api.",
    ),
]
if is_cms_enabled:
    urlpatterns += cms_urls

if is_api_enabled:
    urlpatterns += api_urls