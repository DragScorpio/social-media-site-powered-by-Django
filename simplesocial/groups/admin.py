from django.contrib import admin
from groups import models
# Register your models here.

# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.TabularInline
# he admin interface has the ability to edit models on the same page as a parent model
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember


admin.site.register(models.Group)
