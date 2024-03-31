from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
import datetime


# Реализовать рассылку уведомлений подписчикам после создания новости.
@shared_task
def send_notifications(preview, pk, title, subscribers):
    print('send_notifications')
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def send_week_notification():
    categories = Category.objects.all()
    for category in categories:
        subscribers = category.subscribers.all()
        posts = Post.objects.filter(category=category, date__gte=datetime.datetime.now() - datetime.timedelta(days=7))
        if posts.exists():
            subject = f'Новые статьи в категории {category}'
            html_context = render_to_string(
                'weekly_notifications_email.html',
                {
                    'categ': category,
                    'posts': posts,
                    'link': f'{settings.SITE_URL}/news/'
                }
            )
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[s.email for s in subscribers],
            )
            msg.attach_alternative(html_context, 'text/html')
            msg.send()