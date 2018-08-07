from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
# https://docs.djangoproject.com/en/2.0/ref/urlresolvers/#reverse-lazy
from django.urls import reverse_lazy

from django.views import generic
# https://docs.djangoproject.com/en/2.0/topics/http/views/#django.http.Http404
from django.http import Http404
from django.contrib import messages
# pip install django-braces
from braces.views import SelectRelatedMixin
from posts import forms
from posts import models
# reference the user object on a logged in session
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

class PostList(SelectRelatedMixin, generic.list.ListView):
    model = models.Post
    # http://django-braces.readthedocs.io/en/latest/other.html#selectrelatedmixin
    # A simple mixin which allows you to specify a list or tuple of foreign key fields to perform a select_related
    select_related = ('user','group')


class UserPosts(generic.list.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        try:
            # check that the username is exactly the user who is logged in.
            # create an attribute 'post_user' and assign the object to it
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExit:
            raise Http404
        else:
            return self.post_user.posts.all()


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class PostDetail(SelectRelatedMixin, generic.detail.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.edit.CreateView):
    fields = ('message','group')
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.edit.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)


    def delete(self,*args,**kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
