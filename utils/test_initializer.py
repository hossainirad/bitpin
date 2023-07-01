from faker import Faker
from django.contrib.auth import get_user_model

from article.models import Article

User = get_user_model()
faker = Faker()


def create_user(email):
	user_email = email
	user_obj = User.objects.create_user(email=user_email, username=faker.name(), password=faker.password())
	return user_obj


def create_article(title=None, content=None):
	article_title = title
	article_content = content
	article_obj = Article.objects.create(
		title=article_title,
		content=article_content,
	)
	return article_obj
