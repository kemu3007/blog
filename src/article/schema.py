import graphene
import markdown
from django import forms
from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphql import GraphQLError
from mdx_gfm import GithubFlavoredMarkdownExtension

from .models import Article, Comment, Tag


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article
        exclude = ["last_viewer"]

    html = graphene.NonNull(graphene.String)

    def resolve_html(self, info) -> str:
        return markdown.markdown(self.contents, extensions=[GithubFlavoredMarkdownExtension()])


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment


class Query(graphene.ObjectType):
    articles = graphene.List(graphene.NonNull(ArticleType))
    tags = graphene.List(graphene.NonNull(TagType))

    def resolve_articles(self, info):
        return Article.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("article", "name", "contents")

    def save(self, commit: bool = True):
        return super().save(commit=commit)


class AddComment(DjangoModelFormMutation):
    class Meta:
        form_class = CommentForm
        return_field_name = "comment"

    @classmethod
    def perform_mutate(cls, form, info):
        if ip_address := info.context.META.get("HTTP_X_FORWARDED_FOR"):
            form.instance.ip_address = ip_address
        else:
            raise GraphQLError("IPアドレスが参照できません")
        if info.context.user.is_authenticated:
            form.instance.is_master = True
        return super().perform_mutate(form, info)


class Mutation(graphene.ObjectType):
    add_comment = AddComment.Field()
