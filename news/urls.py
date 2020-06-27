from django.urls import path

from . import views

urlpatterns = [
    path('post/<int:post_id>',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/', views.PostListView.as_view(), name='posts_list'),
]