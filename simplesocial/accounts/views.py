from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from accounts import forms


# Create your views here.
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/flattened-index/
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/generic-editing/#createview
class SignUp(CreateView):
    # https://docs.djangoproject.com/en/2.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_class
    # instantiate a form from UserCreationForm
    form_class = forms.UserCreateForm
    # on a success signup, reverse back to login page
    # delay execution until user hits "submit"
    # after signup, user jumps to login page immediately to log in again:
    success_url = reverse_lazy('login')
    # add app name to settings first so that django knows where to search the next template folder: accounts/templates/...
    template_name = 'accounts/signup.html'
