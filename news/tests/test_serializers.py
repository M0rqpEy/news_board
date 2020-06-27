from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer


class PostSerializerTests(APITestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1', password='password'
        )
        self.post1 = Post.objects.create(
            title='post1', link='url.com', author=self.user1
        )
        self.serializer = PostSerializer(instance=self.post1)


    def test_correct_fields(self):
        data = self.serializer.data
        self.assertEqual(
            list(data.keys()),
            ['id','title', 'link', 'created', 'vote', 'author_name']
        )

    def test_author_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['author_name'], self.user1.username)


class CommentSerializerTests(APITestCase):

    def setUp(self):
        self.user1 = get_user_model().objects.create_user(
            username='user1', password='password'
        )
        self.post1 = Post.objects.create(
            title='post1', link='url.com', author=self.user1
        )
        self.comment1 = Comment.objects.create(
            author=self.user1, content='auth', post=self.post1
        )
        self.serializer = CommentSerializer(instance=self.comment1)


    def test_correct_fields(self):
        data = self.serializer.data
        self.assertEqual(
            list(data.keys()),
            ['id', 'author_name', 'content', 'created']
        )


    def test_author_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(data['author_name'], self.user1.username)