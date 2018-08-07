# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/
# This method will return the currently active user model – the custom user model if one is specified, or User otherwise
from django.contrib.auth import get_user_model
# https://docs.djangoproject.com/en/2.0/topics/auth/default/
# A ModelForm for creating a new user is already built-in
from django.contrib.auth.forms import UserCreationForm

# inherit from a django built-in "Create a new user" form
class UserCreateForm(UserCreationForm):
    #3 built-in fileds: username(from model.User), password1, password2(confirm)
    class Meta:
        fields = ('username','email','password1','password2')
        # to attach custom model, reference:
        # https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms
        model = get_user_model() #defaults to get the current active model

    # setup the label for username field in database, to "Display Name"
    # this also renames the fields in this form being display, so user has better understand
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = "Email Address"
