from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from utils import test_initializer as init


class TestArticleListAPIView(APITestCase):
	def setUp(self) -> None:
		self.url = reverse('article:v1:article_list')
		self.user = init.create_user(email='ali.hossaini34@yahoo.com')
		self.client.force_authenticate(user=self.user)

		self.user1 = init.create_user(email='user1@yahoo.com')
		self.user2 = init.create_user(email='user2@yahoo.com')
		self.user3 = init.create_user(email='user3@yahoo.com')
		self.user4 = init.create_user(email='user4@yahoo.com')
		self.user5 = init.create_user(email='user5@yahoo.com')

		self.article1 = init.create_article(title='article1', content='content1')
		self.article2 = init.create_article(title='article2', content='content2')
		self.article3 = init.create_article(title='article3', content='content3')

	def test_article_list_url(self):
		response = self.client.get(self.url)
		response_json = response.json()
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response_json.get('data').get('count'), 3)
