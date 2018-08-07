from django.shortcuts import render
from groups import models
from django.contrib import messages
# https://docs.djangoproject.com/en/2.0/topics/auth/default/
# for class based views; for function based views, use login_required as decorator instead
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-display/
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/
from django.views import generic
# Calls get() on a given model manager: raises Http404 instead of the model’s DoesNotExist exception.
# https://docs.djangoproject.com/en/2.0/topics/http/shortcuts/
from django.shortcuts import get_object_or_404

from groups.models import Group, GroupMember
# Create your views here.

class CreateGroup(LoginRequiredMixin, generic.edit.CreateView):
    fields = ('name','description')
    model = Group


# https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-display/#detailview
# details of a specific group: posts, member, description, etc.
class SingleGroup(generic.detail.DetailView):
    model = Group

# https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-display/#listview
# on groups page, display a list of all availabe groups:
class ListGroups(generic.list.ListView):
    model = Group


# to join a group, login is firstly required.
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/base/#redirectview
# Redirects to a given URL.
class JoinGroup(LoginRequiredMixin, generic.base.RedirectView):

    # once joining the group(signin), go back to the group detail page
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    # if a person already in that group, no need to join again: raise warning
    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning already a member!')
        else:
            messages.success(self.request, 'You are now a member!')

        return super().get(request,*args,**kwargs)


class LeaveGroup(LoginRequiredMixin, generic.base.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        try:
            membership = models.GroupMember.objects.filter(user=self.request.user,
            group__slug=self.kwargs.get('slug')).get() #try to get the user's membership
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry you are not in this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group!')

        return super().get(request,*args,**kwargs)
