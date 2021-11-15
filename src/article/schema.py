import graphene
import markdown
from graphene_django import DjangoObjectType

from .models import Article, Tag


class ArticleType(DjangoObjectType):
    class Meta:
        model = Article

    html = graphene.NonNull(graphene.String)

    def resolve_html(self, info) -> str:
        return markdown.markdown(self.contents)


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class Query(graphene.ObjectType):
    articles = graphene.List(graphene.NonNull(ArticleType))
    tags = graphene.List(graphene.NonNull(TagType))

    def resolve_articles(self, info):
        return Article.objects.all()

    def resolve_tags(self, info):
        return Tag.objects.all()
