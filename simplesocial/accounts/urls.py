from django.urls import path
# https://docs.djangoproject.com/en/2.0/topics/auth/default/#django.contrib.auth.views.LoginView
# use django built-in LoginView, LogoutView
# SignUp View was customized in accounts/views.py
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    # LoginView:
    # next: The URL to redirect to after successful login. This may contain a query string, too
    # redirect_field_name: The name of a GET field containing the URL to redirect to after login. Defaults to next.
    # the html for LoginView should be placed to registration/login.html by default (however, we
    # point it to accounts/login.html by passing template_name var to it.)
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # LogoutView:
    # next_page: The URL to redirect to after logout. Defaults to settings.LOGOUT_REDIRECT_URL.
    # redirect_field_name: The name of a GET field containing the URL to redirect to after log out. Defaults to next.
    # Overrides the next_page URL if the given GET parameter is passed.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]
