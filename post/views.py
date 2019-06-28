from django.utils import timezone
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.views.generic.edit import ModelFormMixin
from django.contrib import messages

from post.forms import CommentCreateForm
from post.models import Category, Post, Comment


# Create your views here.
def get_error(request):
    messages.error(request, '"https://kemu.site{}"は不正なurlです。'.format(request.get_full_path()))
    return redirect('/')


class PostListView(ListView):
    template_name = 'list.html'
    model = Post
    context_object_name = 'all_post'

    def get_queryset(self):
        category_pk = self.request.GET.get(key='category', default=None)
        if category_pk:
            if Category.objects.filter(pk=category_pk).exists():
                results = Category.objects.get(
                    pk=category_pk).post_set.filter(active=True).order_by('-id')
            else:
                raise 404
        else:
            results = Post.objects.filter(active=True).order_by('-id')
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_category'] = Category.objects.all().order_by('ordering')
        return context


class PostDetailView(ModelFormMixin,DetailView):
    template_name = 'detail.html'
    model = Post
    form_class = CommentCreateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object:
            raise 404
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_list'] = self.object.category.all()
        context['comment_list'] = Comment.get_comment(post_pk=self.object.id).filter(origin=None)
        context['all_category'] = Category.objects.all().order_by('ordering')
        context['days'] = (timezone.localdate() - self.object.modified).days
        return context

    def form_valid(self, form):
        if self.request.POST.get(key='type', default=None) == 'comment':
            post_pk = self.kwargs['pk']
            comment = form.save(commit=False)
            comment.post = Post.objects.get(pk=post_pk)
            comment.created = timezone.localtime()
            comment.save()
        elif self.request.POST.get(key='type', default=None) == 'reply':
            post_pk = self.kwargs['pk']
            origin = self.request.POST.get(key='origin', default=None)
            if origin:
                comment = form.save(commit=False)
                comment.post = Post.objects.get(pk=post_pk)
                comment.origin = Comment.objects.get(pk=origin)
                comment.created = timezone.localtime()
                comment.save()
            else:
                raise 404
        messages.success(self.request, 'メッセージを投稿しました。')
        return redirect(self.request.path)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            self.object = self.get_object()
            return self.form_invalid(form)
