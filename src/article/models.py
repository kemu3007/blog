from django.db import models

from shared.models import BaseModel


class Tag(BaseModel):
    name = models.CharField("タグ", max_length=32)

    def __str__(self) -> str:
        return self.name


class Article(BaseModel):
    title = models.CharField("タイトル", max_length=32)
    contents = models.TextField("記事")
    is_active = models.BooleanField("有効フラグ", default=True)
    tags = models.ManyToManyField("article.Tag", related_name="ref_articles", verbose_name="タグ")

    def __str__(self) -> str:
        return self.title
