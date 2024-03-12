from celery import shared_task
import time

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime, timedelta
from news.models import Category, Post


@shared_task()
def weekly_newsletter():
    today = datetime.now()
    week = today - timedelta(days=7)
    posts = Post.objects.filter(date_creation__gte=week)
    category = set(posts.values_list('category__name', flat=True))
    subscribers = set(Category.objects.filter(name__in=category).values_list('subscribers__email', flat=True))

    html_content = render_to_string('account/email/weekly newsletter.html',

                                    {
                                        'link': settings.SITE_URL,
                                        'posts': posts,
                                    }
                                    )
    msg = EmailMultiAlternatives(
        subject='Новые новости за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@shared_task()
def sending_notifications(pk):
    post = Post.objects.get(pk=pk)
    category = Category.objects.all()
    for cat in category:
        subscriber = cat.subscribers.all()
    html_content = render_to_string('account/email/create_new_post.html',
                                    {'text': f'{post.text[0:25]}',
                                     'link': f'{settings.SITE_URL}/news/{pk}'})
    msg = EmailMultiAlternatives(
        subject=post.title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[s.email for s in subscriber]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


