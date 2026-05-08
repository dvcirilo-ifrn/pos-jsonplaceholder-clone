from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Album, Comment, Photo, Post, Todo, User


def make_user(**kwargs):
    defaults = dict(
        name='Test User', username='testuser', email='test@example.com',
        phone='123', website='example.com', address={}, company={},
    )
    return User.objects.create(**{**defaults, **kwargs})


def make_post(user, **kwargs):
    return Post.objects.create(user=user, title='Test Post', body='Body.', **kwargs)


def make_comment(post, **kwargs):
    return Comment.objects.create(post=post, name='Test', email='c@example.com', body='Body.', **kwargs)


def make_album(user, **kwargs):
    return Album.objects.create(user=user, title='Test Album', **kwargs)


def make_photo(album, **kwargs):
    return Photo.objects.create(
        album=album, title='Test Photo',
        url='http://example.com/img.jpg',
        thumbnailUrl='http://example.com/thumb.jpg',
        **kwargs,
    )


def make_todo(user, **kwargs):
    return Todo.objects.create(user=user, title='Test Todo', completed=False, **kwargs)


class UserTests(APITestCase):
    def setUp(self):
        self.user = make_user()

    def test_list(self):
        r = self.client.get('/users/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/users/{self.user.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['username'], 'testuser')

    def test_create(self):
        payload = {
            'name': 'New User', 'username': 'newuser', 'email': 'new@example.com',
            'phone': '999', 'website': 'new.com', 'address': {}, 'company': {},
        }
        r = self.client.post('/users/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update(self):
        payload = {
            'name': 'Updated', 'username': 'testuser', 'email': 'test@example.com',
            'phone': '123', 'website': 'example.com', 'address': {}, 'company': {},
        }
        r = self.client.put(f'/users/{self.user.pk}/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['name'], 'Updated')

    def test_partial_update(self):
        r = self.client.patch(f'/users/{self.user.pk}/', {'email': 'new@example.com'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['email'], 'new@example.com')

    def test_delete(self):
        r = self.client.delete(f'/users/{self.user.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)

    def test_user_posts(self):
        make_post(self.user)
        make_post(self.user)
        r = self.client.get(f'/users/{self.user.pk}/posts/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)

    def test_user_albums(self):
        make_album(self.user)
        r = self.client.get(f'/users/{self.user.pk}/albums/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_user_todos(self):
        make_todo(self.user)
        r = self.client.get(f'/users/{self.user.pk}/todos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)


class PostTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.post = make_post(self.user)

    def test_list(self):
        r = self.client.get('/posts/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/posts/{self.post.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['user'], self.user.pk)

    def test_create(self):
        r = self.client.post('/posts/', {'user': self.user.pk, 'title': 'New', 'body': 'B'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_update(self):
        r = self.client.put(f'/posts/{self.post.pk}/', {'user': self.user.pk, 'title': 'Up', 'body': 'B'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Up')

    def test_partial_update(self):
        r = self.client.patch(f'/posts/{self.post.pk}/', {'title': 'Patched'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Patched')

    def test_delete(self):
        r = self.client.delete(f'/posts/{self.post.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_post_comments(self):
        make_comment(self.post)
        make_comment(self.post)
        r = self.client.get(f'/posts/{self.post.pk}/comments/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)


class CommentTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.post = make_post(self.user)
        self.comment = make_comment(self.post)

    def test_list(self):
        r = self.client.get('/comments/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/comments/{self.comment.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['post'], self.post.pk)

    def test_create(self):
        payload = {'post': self.post.pk, 'name': 'N', 'email': 'e@e.com', 'body': 'B'}
        r = self.client.post('/comments/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_update(self):
        payload = {'post': self.post.pk, 'name': 'Up', 'email': 'e@e.com', 'body': 'B'}
        r = self.client.put(f'/comments/{self.comment.pk}/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['name'], 'Up')

    def test_partial_update(self):
        r = self.client.patch(f'/comments/{self.comment.pk}/', {'body': 'Patched'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['body'], 'Patched')

    def test_delete(self):
        r = self.client.delete(f'/comments/{self.comment.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)


class AlbumTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.album = make_album(self.user)

    def test_list(self):
        r = self.client.get('/albums/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/albums/{self.album.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['user'], self.user.pk)

    def test_create(self):
        r = self.client.post('/albums/', {'user': self.user.pk, 'title': 'New Album'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)

    def test_update(self):
        r = self.client.put(f'/albums/{self.album.pk}/', {'user': self.user.pk, 'title': 'Updated'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Updated')

    def test_partial_update(self):
        r = self.client.patch(f'/albums/{self.album.pk}/', {'title': 'Patched'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Patched')

    def test_delete(self):
        r = self.client.delete(f'/albums/{self.album.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Album.objects.count(), 0)

    def test_album_photos(self):
        make_photo(self.album)
        make_photo(self.album)
        r = self.client.get(f'/albums/{self.album.pk}/photos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 2)


class PhotoTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.album = make_album(self.user)
        self.photo = make_photo(self.album)

    def test_list(self):
        r = self.client.get('/photos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/photos/{self.photo.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['album'], self.album.pk)

    def test_create(self):
        payload = {
            'album': self.album.pk, 'title': 'New',
            'url': 'http://example.com/a.jpg',
            'thumbnailUrl': 'http://example.com/t.jpg',
        }
        r = self.client.post('/photos/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 2)

    def test_update(self):
        payload = {
            'album': self.album.pk, 'title': 'Updated',
            'url': 'http://example.com/a.jpg',
            'thumbnailUrl': 'http://example.com/t.jpg',
        }
        r = self.client.put(f'/photos/{self.photo.pk}/', payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Updated')

    def test_partial_update(self):
        r = self.client.patch(f'/photos/{self.photo.pk}/', {'title': 'Patched'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['title'], 'Patched')

    def test_delete(self):
        r = self.client.delete(f'/photos/{self.photo.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.count(), 0)


class TodoTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.todo = make_todo(self.user)

    def test_list(self):
        r = self.client.get('/todos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(len(r.data), 1)

    def test_retrieve(self):
        r = self.client.get(f'/todos/{self.todo.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['user'], self.user.pk)

    def test_create(self):
        r = self.client.post('/todos/', {'user': self.user.pk, 'title': 'New', 'completed': False}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)

    def test_update(self):
        r = self.client.put(f'/todos/{self.todo.pk}/', {'user': self.user.pk, 'title': 'Up', 'completed': True}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['completed'], True)

    def test_partial_update(self):
        r = self.client.patch(f'/todos/{self.todo.pk}/', {'completed': True}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['completed'], True)

    def test_delete(self):
        r = self.client.delete(f'/todos/{self.todo.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)
