from django.contrib.auth import views as auth_views
from django.urls import path

from .views import HitCreateView, HitDetailView, HitListView

urlpatterns = [
    path('hits/<int:pk>/', HitDetailView.as_view(), name='hit_detail'),
    path('hits/create/', HitCreateView.as_view(), name='hit_create'),
    path('hits/', HitListView.as_view(), name='hit_list'),
]
