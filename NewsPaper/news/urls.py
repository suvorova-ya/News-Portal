from django.urls import path
from .views import *



urlpatterns = [
   path('', PostList.as_view(),name='post_list'),
   path('search', SearchNews.as_view(), name='search_news'),
   path('<int:pk>', PostDetailView.as_view(), name='post_detail'),
   path('news/create', NewsCreate.as_view(), name='news_create'),
   path('articles/create', NewsCreate.as_view(), name='articles_create'),
   path('news/<int:pk>/update', NewsUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update', NewsUpdate.as_view(), name='articles_update'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
]