from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView

import article.views as article_views
import contact.views as contact_views
import utils.views as utils_views

urlpatterns = [
    path("admin/native/", admin.site.urls),
    path("", article_views.ArticleListView.as_view(), name="article_list"),
    path("contact/", contact_views.ContactView.as_view(), name="contact"),
    path("utils/", utils_views.UtilListView.as_view(), name="utils_list"),
    path("utils/qrcode/", utils_views.QRCodeGeneratorView.as_view(), name="utils_qrcode"),
    path("utils/markdown/", utils_views.MarkdownEditorView.as_view(), name="utils_markdown"),
    path("<str:uuid>/", article_views.ArticleDetailView.as_view(), name="article_detail"),
    path("api/v1/graphql/", GraphQLView.as_view(graphiql=True)),
]
