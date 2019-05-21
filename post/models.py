from django.db import models
from markdownx.models import MarkdownxField


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    def count_post(self):
        return Category.objects.get(id=self.id).post_set.filter(active=True).count()


class Post(models.Model):
    subject = models.CharField(max_length=30)
    contents = MarkdownxField('本文', help_text='Markdown形式で書いてください。')

    active = models.BooleanField()

    created = models.DateField(null=True)
    modified = models.DateField(null=True)

    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.subject

    def is_next_post(self):
        return Post.objects.get(id=self.id + 1)

    def is_past_post(self):
        return Post.objects.get(id=self.id - 1)


class Comment(models.Model):
    send_by = models.CharField('名前', max_length=20)
    created = models.DateTimeField()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    contents = models.TextField()

    def __str__(self):
        return self.id

    @staticmethod
    def get_comment(post_pk):
        return Comment.objects.filter(post=post_pk)
