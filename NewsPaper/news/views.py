from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .filters import PostFilter
from .forms import PostForm
from .tasks import *
from django.contrib.auth.models import Group

class PostList(ListView):
    model = Post
    ordering = ['-date_creation']
    template_name = 'news/news.html'
    context_object_name = 'posts'
    paginate_by = 10


class SearchNews(ListView):
    model = Post
    template_name = 'news/search_news.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'



class NewsCreate(PermissionRequiredMixin,CreateView):
    permission_required = ('news.add_post')
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'news/articles/create/':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'articles/<int:pk>/update' and post.categoryType == 'AR':
            post.save()
        elif self.request.path == '<int:pk>/update' and post.categoryType == 'NW':
            post.save()
        return super().form_valid(form)


# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryList(ListView):
    model = Post
    template_name = 'news/list_category.html'
    context_object_name = 'cat'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date_creation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscriber_user(request,pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
        message = 'Вы успешно отписались от рассылки новостей категории'
    else:
        category.subscribers.add(user)
        message = 'Вы успешно подписались на рассылку новостей категории'

    return render(request, 'news/subscribe.html', {'category': category, 'message': message})

