from typing import Any, Dict

import markdown
from django.db.models.query import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from mdx_gfm import GithubFlavoredMarkdownExtension

from shared.utils import is_uuid

from .models import Article, Comment


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_active=True).prefetch_related(
        Prefetch("ref_comments", Comment.objects.filter(is_active=True))
    )
    template_name = "article/list.html"
    ordering = "-id"


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(is_active=True)
    template_name = "article/detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not is_uuid(self.kwargs["uuid"]):
            return redirect("article_list")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if self.object.last_viewer != request.META.get("HTTP_X_FORWARDED_FOR"):
            self.object.last_viewer = request.META.get("HTTP_X_FORWARDED_FOR")
            self.object.view_count += 1
            self.object.save()
        return response

    def get_object(self, queryset=None) -> Article:
        return get_object_or_404(self.queryset, uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["markdown_contents"] = markdown.markdown(
            self.object.contents, extensions=[GithubFlavoredMarkdownExtension()]
        )
        context_data["comments"] = self.object.ref_comments.filter(is_active=True)
        return context_data
