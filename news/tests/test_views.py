from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from ..views import PostListView, PostDetailView


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
        self.assertEqual(post1.title, response.data[0]['title'])
        self.assertEqual(post2.title, response.data[1]['title'])
        self.assertEqual(len(response.data), Post.objects.count())

    def test_created_post_by_non_login_user(self):
        response = self.client.post(
            reverse('posts_list'),
            data={'title': 'titleasd', "link": "link.com"}
        )
        self.assertEqual(response.status_code, 403)

    def test_create_post_by_logined_user(self):
        self.client.login(username='me', password='me')
        response = self.client.post(
            reverse('posts_list'),
            data={"title": 'title#1', "link": 'http://link.com'}, format='json'
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author,  self.author)
        self.assertEqual(Post.objects.first().title,  'title#1')

class PostDetailViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
                                            username='me', password='me'
        )

    def test_resolve_correct_class(self):
        post = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )
        class_views = resolve(reverse('post_detail', args=[post.id]))
        self.assertEqual(class_views.func.__name__,
                         PostDetailView.as_view().__name__
        )

    def test_get_correct_post_by_id(self):
        post1 = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )
        response = self.client.get(reverse('post_detail', args=[post1.id]))

        self.assertEqual(post1.title, response.data['title'])

    def test_partial_update_post_by_non_login_user(self):
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.patch(
            reverse('post_detail', args=[post1.id]),
            data={'title': 'new title'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_full_update_post_by_non_login_user(self):
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.put(
            reverse('post_detail', args=[post1.id]),
            data={'title': 'new title', 'link': 'url.com'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_partial_update_post_by_logined_user(self):
        self.client.login(username='me', password='me')
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.patch(
            reverse('post_detail', args=[post1.id]),
            data={'title': 'new title'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().author,  self.author)
        self.assertEqual(Post.objects.first().title,  'new title')

    def test_full_update_post_by_logined_user(self):
        self.client.login(username='me', password='me')
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.put(
            reverse('post_detail', args=[post1.id]),
            data={'title': 'new title', 'link': 'http://url1111.com'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().author,  self.author)
        self.assertEqual(Post.objects.first().title,  'new title')
        self.assertEqual(Post.objects.first().link,  'http://url1111.com')

    def test_destroy_post_by_non_login_user(self):
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.delete(
            reverse('post_detail', args=[post1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_destroy_post_by_login_user(self):
        self.client.login(username='me', password='me')
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.delete(
            reverse('post_detail', args=[post1.id]),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Post.objects.count(), 0)