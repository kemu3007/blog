from django.db import models

from shared.models import BaseModel


class Contact(BaseModel):
    name = models.CharField("名前", max_length=32)
    email = models.EmailField("メールアドレス")
    contents = models.TextField("内容")
    ip_address = models.GenericIPAddressField("IPアドレス")

    def __str__(self) -> str:
        return f"{self.name} {self.email}"
