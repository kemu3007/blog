from typing import Any, Dict

import markdown
from django.http.response import Http404
from django.views.generic import DetailView, ListView

from article.models import Article


class ArticleListView(ListView):
    queryset = Article.objects.filter(is_active=True)
    template_name = "article/list.html"
    ordering = "-id"


class ArticleDetailView(DetailView):
    queryset = Article.objects.filter(is_active=True)
    template_name = "article/detail.html"

    def get_object(self, queryset=None) -> Article:
        try:
            article = self.queryset.get(uuid=self.kwargs["uuid"])
        except Article.DoesNotExist:
            raise Http404
        return article

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["markdown_contents"] = markdown.markdown(self.object.contents)
        return context_data
