from django.contrib import admin
from user.models import User
from django.contrib.auth.models import Group, User as UserDefault


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username']

# Register your models here.
admin.site.register(User, UserAdmin)

admin.site.unregister(Group)
admin.site.unregister(UserDefault)