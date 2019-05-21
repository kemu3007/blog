from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from post.models import Post, Category, Comment


# Register your models here.


class PostAdmin(MarkdownxModelAdmin):
    list_display = ['id', 'subject', 'active', 'created', 'modified']
    search_fields = ['active']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'send_by', 'created']


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)
