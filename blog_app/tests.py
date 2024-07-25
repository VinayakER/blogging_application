from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Post, Comment, Like

class BlogAPITestCase(APITestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='testuser2', password='testpass2')
        self.post = Post.objects.create(title='Test Post', content='Test Content', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author=self.user, text='Test Comment')
        self.like = Like.objects.create(post=self.post, created_by=self.user)
        
        # Get JWT token for the user
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_create_post(self):
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'content': 'New Content', 'author': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(id=2).title, 'New Post')
    
    def test_get_posts(self):
        url = reverse('post-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_update_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')
    
    def test_delete_post(self):
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)
    
    def test_create_comment(self):
        url = reverse('comment-list-create', kwargs={'post_id': self.post.pk})
        data = {'text': 'New Comment', 'author': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.get(id=2).text, 'New Comment')
    
    def test_get_comments(self):
        url = reverse('comment-list-create', kwargs={'post_id': self.post.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_like(self):
        url = reverse('like-list-create', kwargs={'post_id': self.post.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 2)
    
    def test_get_likes(self):
        url = reverse('like-list-create', kwargs={'post_id': self.post.pk})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_authentication_required_for_creating_post(self):
        self.client.credentials()  # Remove authentication
        url = reverse('post-list-create')
        data = {'title': 'New Post', 'content': 'New Content'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_required_for_updating_post(self):
        self.client.credentials()  # Remove authentication
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        data = {'title': 'Updated Title', 'content': 'Updated Content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_required_for_deleting_post(self):
        self.client.credentials()  # Remove authentication
        url = reverse('post-detail', kwargs={'pk': self.post.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_required_for_creating_comment(self):
        self.client.credentials()  # Remove authentication
        url = reverse('comment-list-create', kwargs={'post_id': self.post.pk})
        data = {'text': 'New Comment'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authentication_required_for_creating_like(self):
        self.client.credentials()  # Remove authentication
        url = reverse('like-list-create', kwargs={'post_id': self.post.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
