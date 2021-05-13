from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

app_name = 'core'

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("login", views.login_request, name="login"),
    path("register", views.register_request, name="register"),
    path("logout", views.logout_request, name= "logout"),
    path("profile", views.profile, name="profile"),
    path("search", views.search, name="search"),
    path("password_reset", views.password_reset_request, name="password_reset")
    
    
]