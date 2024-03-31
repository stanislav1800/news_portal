import django_filters
from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post
from django import forms

class PostFilter(FilterSet):
    heading = CharFilter(
        label='Заголовок',
        lookup_expr='iregex')

    author = CharFilter(
        label='Автор',
        lookup_expr='iregex')

    date = DateFilter(
        lookup_expr='date__gte',
       widget=forms.DateInput(attrs={'type': 'date'}),
       label='Поиск по дате с'
    )

    class Meta:
        model = Post
        fields = {
           'heading',
           'author',
           'date', 
       }