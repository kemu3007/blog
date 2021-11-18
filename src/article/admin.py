from django.contrib import admin

from .models import Article, Comment, Tag


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "uuid", "is_active", "last_viewer"]
    list_editable = ["is_active"]
    list_filter = ["is_active"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "color"]
    list_editable = ["color"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["article", "name", "contents", "ip_address", "is_active", "is_master"]
    list_editable = ["is_active"]
    list_filter = ["is_active", "is_master"]
