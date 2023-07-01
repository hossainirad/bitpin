from rest_framework import serializers
from django.db.models import Avg

from article.models import Article, ArticleRate


class ArticleListSerializer(serializers.ModelSerializer):
	rated_users_count = serializers.SerializerMethodField()
	current_user_rate = serializers.SerializerMethodField()
	rate_average = serializers.SerializerMethodField()

	class Meta:
		model = Article
		fields = (
			'id',
			'title',
			'content',
			'rated_users_count',
			'current_user_rate',
			'rate_average',
		)

	@staticmethod
	def get_rated_users_count(obj: Article):
		return obj.article_rates.count()

	def get_current_user_rate(self, obj: Article):
		"""
		if user rated this article, return score
		else return null
		"""
		request = self.context.get('request')
		article_rate = obj.article_rates.filter(user=request.user).first()
		if article_rate:
			return article_rate.rate
		return None

	@staticmethod
	def get_rate_average(obj: Article):
		"""
		return average of all rates
		"""
		return obj.article_rates.aggregate(Avg('rate')).get('rate__avg')


class ArticleRateSerializer(serializers.ModelSerializer):
	class Meta:
		model = ArticleRate
		fields = (
			'rate',
		)

	@staticmethod
	def validate_rate(value):
		if not 0 <= value <= 5:
			raise serializers.ValidationError('rate must be between 0 and 5')
		return value
