from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        # title, link, creation date, amount of upvotes, author-name
        fields = ['title', 'link', 'created', 'vote', 'author_name']
