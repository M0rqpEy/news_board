from django.urls import path

from . import views

urlpatterns = [
    path('posts/create', views.PostListView.as_view(), name='post_create'),
    path('posts/', views.PostListView.as_view(), name='posts_list'),
]