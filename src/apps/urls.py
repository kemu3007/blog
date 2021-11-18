from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

import article.views as article_views

urlpatterns = [
    path("admin/native/", admin.site.urls),
    path("", article_views.ArticleListView.as_view(), name="article_list"),
    path("<str:uuid>", article_views.ArticleDetailView.as_view(), name="article_detail"),
    path("api/v1/graphql/", GraphQLView.as_view(graphiql=True)),
]
