from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField("作成日時", auto_now_add=True, blank=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True, blank=True)


class User(AbstractUser):
    pass
