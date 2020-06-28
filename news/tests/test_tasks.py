import time
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from .. tasks import reset_votes
from ..views import PostUpvoteView


class ResetVotesTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            username='me', password='me'
        )
        self.post = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )

    def test_reset_votes(self):
        """
            для теста нужно переключить в файле config/celery.py
            schedule - в 5 секункд
        """
        self.fail('Читать описание теста')
        self.client.login(username='me', password='me')
        self.client.post(reverse('post_upvote', args=[self.post.id]))
        self.assertEqual(Post.objects.first().votes.count(), 1)
        time.sleep(6)
        reset_votes()
        self.assertEqual(Post.objects.first().votes.count(), 0)

