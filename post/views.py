from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from django.contrib import messages

from post.forms import CommentCreateForm
from post.models import Category, Post, Comment


# Create your views here.


class PostListView(ListView):
    template_name = 'list.html'
    model = Post
    context_object_name = 'all_post'

    def get_queryset(self):
        category_pk = self.request.GET.get(key='category', default=None)
        if category_pk:
            results = Category.objects.get(
                pk=category_pk).post_set.filter(active=True)
        else:
            results = Post.objects.filter(active=True)
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_category'] = Category.objects.all().order_by('ordering')
        return context


class PostDetailView(DetailView):
    template_name = 'detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = self.object.category.all()
        context['comment_list'] = Comment.get_comment(post_pk=self.object.id).filter(origin=None)
        context['all_category'] = Category.objects.all().order_by('ordering')
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = 'form.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_category'] = Category.objects.all().order_by('ordering')
        return context

    def form_valid(self, form):
        post_id = self.request.GET.get('post', None)
        origin_id = self.request.GET.get('origin', None)
        if not post_id:
            response = redirect('/')
            messages.error(self.request, 'コメントする記事が見つかりませんでした。')
            return response
        post = Post.objects.get(pk=post_id)
        if origin_id:
            origin = Comment.objects.get(pk=origin_id)
        # 紐づく記事を設定する
        comment = form.save(commit=False)
        comment.post = post
        if origin_id:
            comment.origin = origin
        comment.created = timezone.localtime()
        comment.save()

        response = redirect('/detail/')
        response['location'] += post_id
        # 記事詳細にリダイレクト
        return response
