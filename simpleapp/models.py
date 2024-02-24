from django.db import models
from django.contrib.auth.models import User
#from simpleapp.resources import ITEM, news
from django.urls import reverse

from django import template

article = 'ART'
news = 'NEW'

ITEM = [
    (article, 'Статья'),
    (news, 'Новость')]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username.title()

    
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    item = models.CharField(max_length=3, choices=ITEM, default=news)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = "PostCategory")
    heading = models.CharField(max_length=255)
    text = models.TextField(default = "Текст не введен")

    def __str__(self):
        return f'{self.heading[:10]} {self.date} {self.text[:10]}'
    
    def get_absolute_url(self):
        return f'/news/{self.id}'
        #return reverse('new', args=[str(self.id)])

    def preview(self):
        return self.text[0:123] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)