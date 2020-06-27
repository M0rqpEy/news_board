from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author', read_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'link', 'created', 'vote', 'author_name']


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author', read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'created']
