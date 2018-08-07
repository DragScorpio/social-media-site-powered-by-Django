from django.db import models
# https://docs.djangoproject.com/en/2.0/ref/urlresolvers/
from django.urls import reverse
# https://docs.djangoproject.com/en/2.0/topics/settings/#using-settings-in-python-code
from django.conf import settings

import misaka

from groups.models import Group
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True) #automatically set post time to now()
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        # access base class of post and call save() to save post object to database:
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('posts:single',kwargs={'username':self.user.username, 'pk':self.pk})


    class Meta:
        ordering = ['-created_at']
        # every message is uniquely linked to a user
        unique_together = ['user','message']
