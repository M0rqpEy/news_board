from celery import task

from .models import Post


@task(name='reset_votes')
def reset_votes():
    [post.votes.clear() for post in Post.objects.all()]