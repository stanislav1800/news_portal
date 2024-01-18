from django.db import models
from django.contrib.auth.models import User
from news_portal.resources import ITEM, article


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    
    def update_rating(self):
           
        autor_posts_rating = 0
        autor_comments_rating = 0
        posts_coments_rating = 0

        autor_posts = Post.objects.filter(author = self)
        for p in autor_posts:
            autor_posts_rating += p.rating

        autor_comments = Comment.objects.filter(user = self.user)
        for c in autor_comments:
            autor_comments_rating += c.rating

        posts_comments = Comment.objects.filter(post__author = self)
        for pc in posts_comments:
            posts_coments_rating += pc.rating        
        
        self.user_rating = autor_posts_rating*3 + autor_comments_rating + posts_coments_rating
        self.save()
        
    
class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    item = models.CharField(max_length=3, choices=ITEM, default=article)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField(default = "Текст не введен")
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating+=1
        self.save()
        
    def dislike(self):
        self.rating-=1
        self.save()
        
    def preview(self):
        return self.text[0:124]+'...'
    

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(default = "Коментарий не указан")
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    
    def like(self):
        self.rating+=1
        self.save()
        
    def dislike(self):
        self.rating-=1
        self.save()
