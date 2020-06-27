from django.urls import path

from . import views

urlpatterns = [
    #Posts
    path('posts/<int:post_id>',
         views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/', views.PostListView.as_view(), name='posts_list'),
    #Comments
    path('posts/<int:post_id>/comments/',
         views.CommentListView.as_view(),
         name='comments_list'),
    path('posts/<int:post_id>/comments/<int:comment_id>',
         views.CommentDetailView.as_view(),
         name='comment_detail'),
]


