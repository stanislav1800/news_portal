from django import forms
from .models import Post
class ProductForm(forms.ModelForm):

   class Meta:
       model = Post
       fields = [
           'author',
           'heading',
           'text',
           'category',
       ]
       labels = {
            'author': 'Автор',
            'heading': 'Заголовок',
            'text': 'Текст',
            'category': 'Категория'
        }