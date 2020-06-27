from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from ..serializers import PostSerializer


class PostSerializerTests(APITestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='user1', password='password')
        self.post1 = Post.objects.create(title='post1', link='url.com', author=self.user1)
        self.serializer = PostSerializer(instance=self.post1)


    def test_correct_fields(self):
        data = self.serializer.data
        self.assertEqual(list(data.keys()), ['title', 'link', 'created', 'vote', 'author_name'])


    def test_author_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['author_name'], self.user1.username)