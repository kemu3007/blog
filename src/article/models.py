import uuid

from colorfield.fields import ColorField
from django.db import models

from shared.models import BaseModel


class Tag(BaseModel):
    name = models.CharField("タグ", max_length=32)
    color = ColorField(default="#6c757d")

    def __str__(self) -> str:
        return self.name


class Article(BaseModel):
    uuid = models.UUIDField("UUID", default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField("タイトル", max_length=32)
    contents = models.TextField("記事")
    is_active = models.BooleanField("有効フラグ", default=True)
    tags = models.ManyToManyField("article.Tag", related_name="ref_articles", verbose_name="タグ", blank=True)

    def __str__(self) -> str:
        return self.title


class Comment(BaseModel):
    article = models.ForeignKey("article.Article", on_delete=models.CASCADE, related_name="ref_comments")
    ip_address = models.GenericIPAddressField("IPアドレス")
    name = models.CharField("名前", max_length=32)
    contents = models.CharField("内容", max_length=255)
    is_active = models.BooleanField("有効フラグ", default=True)
    is_master = models.BooleanField("管理者からのコメント", default=False)

    def __str__(self) -> str:
        return self.contents
