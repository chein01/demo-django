from django.db import models


class BaseDateTime(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created Time")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Updated Time")

    class Meta:
        abstract = True
