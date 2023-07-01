from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from article.api.v1.views import ArticleListAPIView, ArticleRateAPIView
from utils import test_initializer as init


class TestArticleListAPIView(APITestCase):
	def setUp(self) -> None:
		self.url = reverse('article:v1:article_list')
		self.user = init.create_user(email='ali.hossaini34@yahoo.com')
		self.client.force_authenticate(user=self.user)

		self.article1 = init.create_article(title='article1', content='content1')
		self.article2 = init.create_article(title='article2', content='content2')
		self.article3 = init.create_article(title='article3', content='content3')

	def test_article_list_success(self):
		response = self.client.get(self.url)
		response_json = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_json.get('data').get('count'), 3)
		self.assertIn('id', response_json.get('data').get('results')[0].keys())
		self.assertIn('title', response_json.get('data').get('results')[0].keys())
		self.assertIn('content', response_json.get('data').get('results')[0].keys())
		self.assertIn('rated_users_count', response_json.get('data').get('results')[0].keys())
		self.assertIn('current_user_rate', response_json.get('data').get('results')[0].keys())
		self.assertIn('rate_average', response_json.get('data').get('results')[0].keys())

	def test_resolve_url(self):
		resolver = resolve('/api/v1/article/article-list/')
		self.assertEqual(resolver.view_name, 'article:v1:article_list')
		self.assertEqual(resolver.func.view_class, ArticleListAPIView)
		self.assertEqual(resolver.namespace, 'article:v1')
		self.assertEqual(resolver.url_name, 'article_list')


class TestArticleRateAPIView(APITestCase):
	def setUp(self) -> None:
		self.user = init.create_user(email='exampleuser@yahoo.com')
		self.client.force_authenticate(user=self.user)
		self.user1 = init.create_user(email='user1@yahoo.com')
		self.user2 = init.create_user(email='user2@yahoo.com')
		self.user3 = init.create_user(email='user3@yahoo.com')
		self.user4 = init.create_user(email='user4@yahoo.com')
		self.user5 = init.create_user(email='user5@yahoo.com')

		self.article = init.create_article(title='article1', content='content1')

	def test_article_rate_success(self):
		url = reverse('article:v1:article_rate', kwargs={'article_id': self.article.id})
		response = self.client.post(url, data={'rate': 5})
		self.assertEqual(response.status_code, 201)
		article_rate_obj = self.article.article_rates.filter(user=self.user).last()
		self.assertEqual(article_rate_obj.rate, 5)

	def test_resolve_url(self):
		resolver = resolve('/api/v1/article/1/rate/')
		self.assertEqual(resolver.view_name, 'article:v1:article_rate')
		self.assertEqual(resolver.func.view_class, ArticleRateAPIView)
		self.assertEqual(resolver.namespace, 'article:v1')
		self.assertEqual(resolver.url_name, 'article_rate')
