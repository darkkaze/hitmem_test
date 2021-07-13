
from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (HitmenCreateView, HitmenDetailView, HitmenListView,
                    SignUpView, home_redirect)

urlpatterns = [
    path('hitmen/<int:pk>/', HitmenDetailView.as_view(), name='hitmen_detail'),
    path('hitmen/create/', HitmenCreateView.as_view(), name='hitmen_create'),
    path('hitmen/', HitmenListView.as_view(), name='hitmen_list'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.logout_then_login, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('', home_redirect, name='home'),
]
