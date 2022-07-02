from django.contrib import admin
from task.models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'status']
# Register your models here.
admin.site.register(Task, TaskAdmin)