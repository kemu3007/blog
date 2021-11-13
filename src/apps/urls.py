from django.contrib import admin
from django.urls import path

import article.views as article_views

urlpatterns = [
    path("admin/native/", admin.site.urls),
    path("", article_views.ArticleListView.as_view(), name="article_list"),
    path("<int:pk>", article_views.ArticleDetailView.as_view(), name="article_detail"),
]
