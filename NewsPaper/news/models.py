from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.user.username

    def update_rating(self):
        rating_post = self.post_set.aggregate(rp=Coalesce(Sum("rating"), 0)).get('rp')
        rating_comment = self.user.comment_set.aggregate(rc=Coalesce(Sum("rating"), 0)).get('rc')
        comment_post_aut = self.post_set.aggregate(rpa=Coalesce(Sum('comment__rating'), 0)).get('rpa')
        self.rating = rating_post * 3 + rating_comment + comment_post_aut
        self.save()


    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=160, unique=True, null=True, verbose_name='slug')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', verbose_name='Подписчики')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):

    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, verbose_name="Автор")
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=NEWS,
                                    verbose_name="Тип категории")
    date_creation = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory', verbose_name="Категория")
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    rating = models.IntegerField(default=0, verbose_name="Рейтинг")

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{self.title}: {self.text[:20]}'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def save(self, *args, **kwargs):
        """Переопределение метода сохранения модели с очисткой кэша."""
        super().save(*args, **kwargs)  # Сначала сохраняем объект
        cache.delete(f'post-{self.pk}')  # Затем удаляем его из кэша

    def delete(self, *args, **kwargs):
        """Переопределение метода удаления модели с очисткой кэша."""
        cache.delete(f'post-{self.pk}')  # Удаляем кэш перед удалением объекта
        super().delete(*args, **kwargs)  # Затем удаляем объект из базы данных

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Статья')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name = "Категория новости"
        verbose_name_plural = "Категории новостей"

    def __str__(self):
        return f'Текст: {self.post} Категория: {self.category}'

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    data_comment = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}__{self.text}__{self.rating}'
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"