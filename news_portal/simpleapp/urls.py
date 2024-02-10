from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch


urlpatterns = [
    path("", PostList.as_view(), name='news'),
    #path('post/', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view(), name='new'), 
    path('search/', PostSearch.as_view(), name='news_search'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('articles/create/', PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='articles_edit'),
]
