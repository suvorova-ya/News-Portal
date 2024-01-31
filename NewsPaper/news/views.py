from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm

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



class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'news/articles/create/':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)

class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == 'news/articles/<int:pk>/update' and post.categoryType == 'AR':
            post.save()
        elif self.request.path == 'news/<int:pk>/update' and post.categoryType == 'NW':
            post.save()
        return super().form_valid(form)


# Представление удаляющее товар.
class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('post_list')