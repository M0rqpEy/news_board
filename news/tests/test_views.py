from django.contrib.auth import get_user_model
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase

from ..models import Post, Comment
from ..views import (
    PostListView,
    PostDetailView,
    CommentListView,
    CommentDetailView
)


class PostListViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            username='me', password='me'
        )

    def test_resolve_correct_class(self):
        class_views = resolve(reverse('posts_list'))
        self.assertEqual(
            class_views.func.__name__,
            PostListView.as_view().__name__
        )

    def test_get_correct_all_posts(self):
        post1 = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )
        post2 = Post.objects.create(
            title='post2', link='url.com', author=self.author
        )
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


class PostUpvoteViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
                                            username='me', password='me'
        )

    def test_cannot_non_logined_user_upvote(self):
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.post(reverse('post_upvote', args=[post1.id]))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.first().votes.count(), 0)

    def test_can_logined_user_upvote(self):
        self.client.login(username='me', password='me')
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.post(reverse('post_upvote', args=[post1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().votes.count(), 1)

    def test_cannot_logined_user_upvote_twice(self):
        self.client.login(username='me', password='me')
        post1 = Post.objects.create(
            title='post1', link='http://url.com', author=self.author
        )
        response = self.client.post(reverse('post_upvote', args=[post1.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.first().votes.count(), 1)

        response = self.client.post(reverse('post_upvote', args=[post1.id]))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Post.objects.first().votes.count(), 1)


class CommentListViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            username='me', password='me'
        )
        self.author_comment = get_user_model().objects.create_user(
            username='u', password='u'
        )
        self.post = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )

    def test_resolve_correct_class(self):
        class_views = resolve(reverse('comments_list', args=[self.post.id]))
        self.assertEqual(
            class_views.func.__name__, CommentListView.as_view().__name__
        )

    def test_get_correct_all_comments(self):
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.get(
            reverse('comments_list', args=[self.post.id])
        )
        self.assertEqual(comment1.content, response.data[0]['content'])
        self.assertEqual(
            comment1.author.username,
            response.data[0]['author_name']
        )

    def test_created_post_by_non_login_user(self):
        response = self.client.post(
            reverse('comments_list', args=[self.post.id]),
            data={'content': 'titleasd'}
        )
        self.assertEqual(response.status_code, 403)

    def test_create_post_by_logined_user(self):
        self.client.login(username='u', password='u')
        response = self.client.post(
            reverse('comments_list', args=[self.post.id]),
            data={'content': 'titleasd'}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().author,  self.author_comment)
        self.assertEqual(Comment.objects.first().content,  'titleasd')
        self.assertEqual(Comment.objects.first().post,  self.post)


class CommentDetailViewTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.author = get_user_model().objects.create_user(
            username='me', password='me'
        )
        self.author_comment = get_user_model().objects.create_user(
            username='u', password='u'
        )
        self.post = Post.objects.create(
            title='post1', link='url.com', author=self.author
        )

    def test_resolve_correct_class(self):
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        class_views = resolve(
            reverse('comment_detail', args=[self.post.id, comment1.id])
        )
        self.assertEqual(
            class_views.func.__name__,
            CommentDetailView.as_view().__name__
        )

    def test_get_correct_comment_by_id(self):
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.get(
            reverse('comment_detail', args=[self.post.id, comment1.id])
        )
        self.assertEqual(comment1.content, response.data['content'])

    def test_full_update_post_by_non_login_user(self):
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.put(
            reverse('comment_detail', args=[self.post.id, comment1.id]),
            data={'content': 'new con'},
            format='json',
        )

        self.assertEqual(response.status_code, 403)

    def test_full_update_post_by_logined_user(self):
        self.client.login(username='u', password='u')
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.put(
            reverse('comment_detail', args=[self.post.id, comment1.id]),
            data={'content': 'new con'},
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.first().author,  self.author_comment)
        self.assertEqual(Comment.objects.first().content,  'new con')
        self.assertEqual(Comment.objects.first().post, self.post)

    def test_destroy_post_by_non_login_user(self):
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.delete(
            reverse('comment_detail', args=[self.post.id, comment1.id]),
        )
        self.assertEqual(response.status_code, 403)

    def test_destroy_post_by_login_user(self):
        self.client.login(username='u', password='u')
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.delete(
            reverse('comment_detail', args=[self.post.id, comment1.id]),
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), 0)

    def test_destroy_post_by_login_user_and_not_owner(self):
        self.client.login(username='me', password='me')
        comment1 = Comment.objects.create(
            author=self.author_comment,
            content='help',
            post=self.post
        )
        response = self.client.delete(
            reverse('comment_detail', args=[self.post.id, comment1.id]),
        )
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(response.status_code, 403)
