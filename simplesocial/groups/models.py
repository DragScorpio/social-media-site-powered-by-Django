from django.db import models
from django.urls import reverse
# https://docs.djangoproject.com/en/2.0/ref/utils/
# Converts spaces to hyphens. Removes characters that aren’t alphanumerics,
# underscores, or hyphens. Converts to lowercase.
# Also strips leading and trailing whitespace.
from django.utils.text import slugify

# misaka features fast HTML renderer and functionality to make custom renderers
import misaka
# reference the user model, either customized, or User as default
from django.contrib.auth import get_user_model
# Create your models here.

# get the current active user model
User = get_user_model()

# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/
# register custom template tags for future use:
from django import template
register = template.Library()

# main models here: each model maps to a single database table.
# https://docs.djangoproject.com/en/2.0/topics/db/models/
# model writing steps:
# 1.Each model is a Python class that subclasses django.db.models.Model.
# 2.Each attribute of the model represents a database field.
# 3.plus, applying Django's built-in automatically-generated database-access API

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True) #url code does not have to be all ascii: as long as unicode
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)

    # https://docs.djangoproject.com/en/2.0/topics/db/examples/many_to_many/
    # ManyToMany: Group can have many members/users, a member can belong to many groups
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ManyToManyField
    # https://docs.djangoproject.com/en/2.0/ref/models/fields/#django.db.models.ManyToManyField.through
    # through options indicate the intermediate table between User and Group: GroupMember
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # convert name to unicode (lowercase, dash-replace-space, no trailing whitespaces...):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        #get the url of it by reverse analyze url name: single, in groups/urls.py
        return reverse('groups:single',kwargs={'slug':self.slug})


    class Meta:
        ordering = ['name']




# a specific group-member belongs to only this group, and is a unique user
class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        # print the built-in field, username, of model User
        return self.user.username

    class Meta:
        unique_together = ('group','user')
