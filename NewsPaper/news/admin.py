from django.contrib import admin
from .models import Category, Post, PostCategory, Comment,Autor


admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Autor)


