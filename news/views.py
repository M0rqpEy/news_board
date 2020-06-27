from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated
)
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import F

from .permissions import IsOwnerOrReadOnly
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


# Create your views here.
class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_url_kwarg = 'post_id'
    permission_classes = [IsOwnerOrReadOnly]


class PostUpvoteView(APIView):
    allowed_methods = ['POST']
    permission_classes = [IsAuthenticated]

    def post(self, request, **kwargs):
        post_id = self.kwargs["post_id"]
        post_votes_id = Post.objects.filter(id=post_id).prefetch_related('votes')

        if request.user not in post_votes_id.first().votes.all():
            post_votes_id.first().votes.add(request.user)
            return Response({"detail": "Success"}, status=status.HTTP_200_OK)
        return Response(
            {"detail": "You cannot upvote twice"}, status=status.HTTP_400_BAD_REQUEST
        )


class CommentListView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])
