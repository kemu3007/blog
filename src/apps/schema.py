import graphene

from article.schema import Query as ArticleQuery


class Query(ArticleQuery):
    pass


schema = graphene.Schema(query=Query)
