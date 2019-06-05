from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework_jwt.settings import api_settings

from django.contrib.auth import get_user_model

from postings.models import BlogPost


User = get_user_model()

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER


class BlogPostAPITestCase(APITestCase):

  def setUp(self):
    # Create user
    user = User(username='test_user', email='test@test.com')
    user.set_password('dfasdfasdfas')
    user.save()
    # Create blog posts
    blog_post = BlogPost.objects.create(
      user=user,
      title='New title',
      content='Some random content.'
    )

  def test_single_user(self):
    user_count = User.objects.count()
    self.assertEqual(user_count, 1)

  def test_single_post(self):
    post_count = BlogPost.objects.count()
    self.assertEqual(post_count, 1)

  def test_get_posts(self):
    data = {}
    url = api_reverse('api-postings:post-listcreate')
    response = self.client.get(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_create_post(self):
    data = {
      'title': 'Some random title for testing',
      'content': 'Super random'
    }
    url = api_reverse('api-postings:post-listcreate')
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_get_item(self):
    blog_post = BlogPost.objects.first()
    data = {}
    url = blog_post.get_api_url()
    response = self.client.get(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_update_post(self):
    blog_post = BlogPost.objects.first()
    url = blog_post.get_api_url()
    data = {
      'title': 'Some random title for testing123',
      'content': 'Super random'
    }
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

  def test_create_post_with_user(self):
    user_obj = User.objects.first()
    payload = payload_handler(user_obj)
    token_resp = encode_handler(payload)
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_resp)

    data = {
      'title': 'Some random title for testing',
      'content': 'Super random'
    }
    url = api_reverse('api-postings:post-listcreate')
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

  def test_update_post_with_user(self):
    blog_post = BlogPost.objects.first()
    url = blog_post.get_api_url()
    data = {
      'title': 'Some random title for testing123',
      'content': 'Super random'
    }
    user_obj = User.objects.first()
    payload = payload_handler(user_obj)
    token_resp = encode_handler(payload)
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_resp)

    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)

  def test_user_ownership(self):
    owner = User.objects.create(username='testuser123')
    blog_post = BlogPost.objects.create(
      user=owner,
      title='New title123123123',
      content='Some random content.'
    )

    user_obj = User.objects.first()
    self.assertNotEqual(user_obj.username, owner.username)

    payload = payload_handler(user_obj)
    token_resp = encode_handler(payload)
    self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_resp)

    url = blog_post.get_api_url()
    data = {
      'title': 'Some rando title for testing1',
      'content': 'Super random'
    }
    response = self.client.put(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

  def test_user_login_and_update_post(self):
    data = {
      'username': 'test_user',
      'password': 'dfasdfasdfas'
    }
    url = api_reverse('api-login')
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    token = response.data.get('token')
    if token is not None:
      blog_post = BlogPost.objects.first()
      url = blog_post.get_api_url()
      data = {
        'title': 'Some random title for testing123',
        'content': 'Super random'
      }
      self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
      response = self.client.put(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)
