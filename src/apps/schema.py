import graphene

from article.schema import Mutation as ArticleMutation
from article.schema import Query as ArticleQuery
from contact.schema import Mutation as ContactMutation


class Query(ArticleQuery):
    pass


class Mutation(ArticleMutation, ContactMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
