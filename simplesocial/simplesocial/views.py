from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse

# https://docs.djangoproject.com/en/2.0/ref/class-based-views/base/#templateview
# https://docs.djangoproject.com/en/2.0/ref/class-based-views/flattened-index/
# HomePage class inherits from TemplateView

# Renders a given template, with the context containing parameters captured in the URL.
class TestPage(TemplateView):
    template_name = 'test.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))

        return super().get(request,*args,**kwargs)
