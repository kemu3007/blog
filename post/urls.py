from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from post.views import PostDetailView, PostListView, CommentCreateView

urlpatterns = [
    path(r'', PostListView.as_view()),
    path(r'form/', CommentCreateView.as_view()),
    path(r'detail/<pk>', PostDetailView.as_view()),
]

# 開発環境でのメディアファイルの配信設定
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
