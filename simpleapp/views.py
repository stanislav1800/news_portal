from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import ProductForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import redirect

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

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribed'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        email =user.email
        message = 'Вы подписались на категорию'
        html = render_to_string('subscribe.html',{'category': category, 'message': message})
        msg = EmailMultiAlternatives(subject=f' Вы подписались на категорию',
                                     body='',
                                     from_email='stasiklim18@yandex.ru',
                                     to=[email,],)
        msg.attach_alternative(html,'text/html')
        try:
            msg.send()
        except Exception as e:
            print(e)
        return redirect('news')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category.subscribers.filter(id=user.id).exists():
        category.subscribers.remove(user)
    return redirect('news')