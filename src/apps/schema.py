import graphene

from article.schema import Mutation as ArticleMutation
from article.schema import Query as ArticleQuery


class Query(ArticleQuery):
    pass


class Mutation(ArticleMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
