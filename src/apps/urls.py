from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib.sitemaps.views import sitemap
from django.urls import path
from graphene_django.views import GraphQLView

import apps.views as apps_views
import article.views as article_views
import contact.views as contact_views
import utils.views as utils_views
from apps.admin import AutoGenerateAdminSite

from .sites import ArticleRssFeed, sitemaps

urlpatterns = (
    [
        path("admin/native/", AutoGenerateAdminSite().urls),
        path("profile/", apps_views.ProfileView.as_view(), name="profile"),
        path("sitemap.xml/", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
        path("rss/", ArticleRssFeed(), name="rss"),
        path("", article_views.ArticleListView.as_view(), name="article_list"),
        path("contact/", contact_views.ContactView.as_view(), name="contact"),
        path("utils/", utils_views.UtilListView.as_view(), name="utils_list"),
        path("utils/qrcode/", utils_views.QRCodeGeneratorView.as_view(), name="utils_qrcode"),
        path("utils/markdown/", utils_views.MarkdownEditorView.as_view(), name="utils_markdown"),
        path("utils/rakuten/", login_required(utils_views.RakutenConverterView.as_view()), name="utils_rakuten"),
        path(
            "utils/mufj_debit/", login_required(utils_views.MUFJDebitConverterView.as_view()), name="utils_mufj_debit"
        ),
        path("utils/csv_to_md/", utils_views.CSVTOMDConvertorView.as_view(), name="utils_csv_to_md"),
        path("<str:uuid>/", article_views.ArticleDetailView.as_view(), name="article_detail"),
        path("api/v1/graphql/", GraphQLView.as_view(graphiql=True)),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
