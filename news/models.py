from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    vote = models.PositiveSmallIntegerField(default=0)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='comments'
    )
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )

    def __str__(self):
        return self.content[:20]
