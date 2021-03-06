from django.contrib import admin
from groups import models
# Register your models here.

# https://docs.djangoproject.com/en/2.1/ref/contrib/admin/#django.contrib.admin.TabularInline
# he admin interface has the ability to edit models on the same page as a parent model
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

# customize administration site: add search bar + filter, display fields by listing, and make them listable.
class GroupAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    list_filter = ['name',]
    list_display = ['name','slug',]
    # display first before making it editable
    # list_editable = ['name',]

admin.site.register(models.Group,GroupAdmin)
