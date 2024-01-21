from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Autor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        rating_post = self.post_set.aggregate(rp=Coalesce(Sum("rating"), 0)).get('rp')
        rating_comment = self.user.comment_set.aggregate(rc=Coalesce(Sum("rating"), 0)).get('rc')
        comment_post_aut = self.post_set.comment.aggregate(rpa=Coalesce(Sum('comment__rating'), 0)).get()

        self.rating = rating_post * 3 + rating_comment + comment_post_aut
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)


class Post(models.Model):

    autor = models.ForeignKey(Autor, on_delete=models.CASCADE,)
    ARTICLE = 'AR'
    NEWS = 'NW'
    CATEGORY_CHOICES = (
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    )
    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE,
                                    verbose_name="Тип категории")
    date_creation = models.DateField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=120)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:126]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    data_comment = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()