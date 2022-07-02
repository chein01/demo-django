from django.db import models
from base.models import BaseDateTime
from task.choices import STATUS_TASK, PENDING
from user.models import User
# Create your models here.


class Task(BaseDateTime):
    status = models.CharField(
        max_length=10, choices=STATUS_TASK, default=PENDING, verbose_name="Status")
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(
        blank=True, max_length=255, verbose_name="Description")
    task = models.TextField(verbose_name="Task")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="User")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "d_task"
        verbose_name = "Task"
        verbose_name_plural = "Task"
