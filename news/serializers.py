from rest_framework import serializers

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author', read_only=True
    )
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'link', 'created', 'votes', 'author_name']

    def get_votes(self, obj):
        return obj.votes.count()


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(
        source='author', read_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'created']
