from django.contrib import admin

from .models import User


@admin.action(description="Mark selected stories as published")
def make_published(modeladmin, request, queryset):
    queryset.update(status="p")


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
