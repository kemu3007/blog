from typing import Any, Dict

import markdown
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView
from mdx_gfm import GithubFlavoredMarkdownExtension

from article.models import Article
from shared.utils import is_uuid


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_active=True)
    template_name = "article/list.html"
    ordering = "-id"


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(is_active=True)
    template_name = "article/detail.html"

    def dispatch(self, request, *args, **kwargs):
        if not is_uuid(self.kwargs["uuid"]):
            return redirect("article_list")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Article:
        return get_object_or_404(self.queryset, uuid=self.kwargs["uuid"])

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["markdown_contents"] = markdown.markdown(
            self.object.contents, extensions=[GithubFlavoredMarkdownExtension()]
        )
        return context_data
