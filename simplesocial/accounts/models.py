from django.db import models
from django.contrib import auth

# Create your models here.
# https://docs.djangoproject.com/en/2.0/ref/contrib/auth/
# https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin
class User(auth.models.User, auth.models.PermissionsMixin):
    #default required fields: username, password
    def __str__(self):
        # username is required and built-in in User model
        return "@{}".format(self.username)
