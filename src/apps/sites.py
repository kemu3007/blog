from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed
from django.shortcuts import resolve_url
from django.urls import reverse_lazy

from article.models import Article


class ArticleRssFeed(Feed):
    title = "kemuのブログ"
    link = reverse_lazy("article_list")

    def items(self):
        return Article.objects.all()

    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.contents[:100].replace("#", "")

    def item_link(self, item: Article):
        return resolve_url("article_detail", uuid=item.uuid)


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
