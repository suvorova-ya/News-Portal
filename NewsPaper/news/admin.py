from django.contrib import admin
from .models import Category, Post, PostCategory, Comment, Autor


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)

class CategorylineAdmin(admin.TabularInline):
    model = Post.category.through


class PostAdmin(admin.ModelAdmin):
    model = Post
    fields = ['autor', 'title', 'categoryType', 'text']
    inlines = (CategorylineAdmin,)

admin.site.register(Post, PostAdmin)


admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Autor)


