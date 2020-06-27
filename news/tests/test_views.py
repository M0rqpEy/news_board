from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from ..views import PostListView


class PostListViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(username='me', password='me')

    def test_resolve_correct_class(self):
        class_views = resolve(reverse('posts_list'))
        self.assertEqual(class_views.func.__name__, PostListView.as_view().__name__)

    def test_get_correct_all_posts(self):
        post1 = Post.objects.create(title='post1', link='url.com', author=self.author)
        post2 = Post.objects.create(title='post2', link='url.com', author=self.author)
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(len(response.data), Post.objects.count())

    def test_created_post_by_non_login_user(self):
        response = self.client.post(
            reverse('post_create'),
            data={'title': 'titleasd', "link": "link.com"}
        )
        self.assertEqual(response.status_code, 403)

    def test_create_post_by_logined_user(self):
        self.client.login(username='me', password='me')
        response = self.client.post(
            reverse('post_create'),
            data={"title": 'title#1', "link": 'http://link.com'}, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author,  self.author)
        self.assertEqual(Post.objects.first().title,  'title#1')
