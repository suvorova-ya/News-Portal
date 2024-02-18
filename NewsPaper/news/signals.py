from django.conf import settings
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def notify_post_create(sender, instance, action, **kwargs):
    if action == 'post_add':
        category = instance.category.all()
        for cat in category:
            subscribers = cat.subscribers.all()
            html_content = render_to_string('account/email/create_new_post.html',
                                            {'text': f'{instance.text[0:25]}',
                                                    'link': f'{settings.SITE_URL}/news/{instance.pk}'})
            msg = EmailMultiAlternatives(
                subject=instance.title,
                body=instance.text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email for s in subscribers]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()



