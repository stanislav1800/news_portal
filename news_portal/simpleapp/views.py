from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import ProductForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

class PostList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

class PostCreate(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    context_object_name = 'news'
    permission_required = 'simpleapp.add_post'
    form_class = ProductForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news')
    
    def form_valid(self, form):
        Post = form.save(commit=False)
        print(self.request.path)
        if self.request.path=='/news/articles/create/':
            Post.item = 'ART'
        Post.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = 'simpleapp.change_post'
    form_class = ProductForm
    model = Post
    template_name = 'news_edit.html'

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = 'simpleapp.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context