import django_filters
import pytz
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from django.views.decorators.cache import cache_page

#from .forms import PostForm
from .models import Post, Category
from django.http import HttpResponse
from django.views import View
#from .tasks import hello, shared_task, printer
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils import timezone
from .forms import PostForm


# Create your views here.


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-time_in'
    paginate_by = 2


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['current_time'] = timezone.now()
        return context
    
def author_now(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        user.groups.add(author_group)
    return redirect('post_list')

class NewsDetail(DeleteView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
    
        return obj


class NewsCreate(CreateView):
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'posts'
    permission_required = ('news_portal.add_post')
    fields='__all__'
    uccess_url = reverse_lazy('post')
    
    

class NewsUpload(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    context_object_name = 'posts'
    permission_required = ('news_portal.change_post')
    success_url = reverse_lazy('post_list')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'posts'
    success_url = reverse_lazy('post_list')