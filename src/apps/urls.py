from django.contrib import admin
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import resolve_url
from django.urls import path
from graphene_django.views import GraphQLView

import article.views as article_views
import contact.views as contact_views
import utils.views as utils_views
from article.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.all()

    def location(self, obj: Article):
        return resolve_url("article_detail", uuid=obj.uuid)

    def lastmod(self, obj: Article):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    """
    静的ページのサイトマップ
    """

    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ["article_list", "contact", "utils_list", "utils_qrcode", "utils_markdown"]

    def location(self, item):
        return resolve_url(item)


sitemaps = {
    "articles": ArticleSitemap,
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("admin/native/", admin.site.urls),
    path("sitemap.xml/", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("", article_views.ArticleListView.as_view(), name="article_list"),
    path("contact/", contact_views.ContactView.as_view(), name="contact"),
    path("utils/", utils_views.UtilListView.as_view(), name="utils_list"),
    path("utils/qrcode/", utils_views.QRCodeGeneratorView.as_view(), name="utils_qrcode"),
    path("utils/markdown/", utils_views.MarkdownEditorView.as_view(), name="utils_markdown"),
    path("<str:uuid>/", article_views.ArticleDetailView.as_view(), name="article_detail"),
    path("api/v1/graphql/", GraphQLView.as_view(graphiql=True)),
]
