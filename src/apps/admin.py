from typing import Type

from colorfield.fields import ColorField
from django.apps import apps
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db import models


def get_admin_model(model: Type[models.Model]) -> Type[ModelAdmin]:
    list_display_fields = [
        models.CharField,
        models.IntegerField,
        models.PositiveIntegerField,
        models.ForeignKey,
        models.BooleanField,
        ColorField,
    ]
    list_editable_field = [models.IntegerField, models.PositiveIntegerField, models.BooleanField, ColorField]
    list_display = ["pk"]
    list_editable = []
    for field in model._meta.fields:
        if type(field) in list_display_fields:
            list_display.append(field.name)
        if type(field) in list_editable_field and field.editable:
            list_editable.append(field.name)
    return type(
        f"{model._meta.model_name}ModelAdmin",
        (ModelAdmin,),
        {"list_display": list_display, "list_editable": list_editable, "ordering": model._meta.ordering or ["pk"]},
    )


class AutoGenerateAdminSite(AdminSite):
    display_app_list = ["sites", "shared", "article", "contact"]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._registry = {model: get_admin_model(model)(model=model, admin_site=self) for model in apps.get_models()}

    def _build_app_dict(self, request):
        app_dict = super()._build_app_dict(request)
        return dict(filter(lambda app: app[0] in self.display_app_list, app_dict.items()))
