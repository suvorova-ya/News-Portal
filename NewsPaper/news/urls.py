from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('search', SearchNews.as_view(), name='search_news'),
    path('<int:pk>', cache_page(60 * 5)(PostDetailView.as_view()), name='post_detail'),
    path('create', NewsCreate.as_view(), name='news_create'),
    path('articles/create', NewsCreate.as_view(), name='articles_create'),
    path('<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
    path('articles/<int:pk>/update', NewsUpdate.as_view(), name='articles_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('category/<int:pk>', cache_page(60 * 5)(CategoryList.as_view()), name='category_list'),  # фильтр по категориям
    path('category/<int:pk>/subscribe', subscriber_user, name='subscriber_user'),  # подписка на категорию

]
