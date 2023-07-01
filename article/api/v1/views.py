from rest_framework.generics import ListAPIView
from rest_framework.views import APIView, status
from drf_spectacular.utils import extend_schema

from article.api.v1.serializers import ArticleListSerializer, ArticleRateSerializer
from article.models import Article, ArticleRate
from utils.api.error_objects import ErrorObject
from utils.api.mixins import BadRequestSerializerMixin
from utils.api.responses import error_response, success_response
from rest_framework.permissions import IsAuthenticated


class ArticleListAPIView(ListAPIView):
	serializer_class = ArticleListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		return Article.objects.all()

	@extend_schema(
		request=None,
		responses={200: ArticleListSerializer},
		auth=None,
		operation_id='ArticleList',
		tags=['Article'],
	)
	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)


class ArticleRateAPIView(BadRequestSerializerMixin, APIView):
	serializer_class = ArticleRateSerializer
	permission_classes = [IsAuthenticated]

	@extend_schema(
		request=ArticleRateSerializer,
		responses={201: None},
		auth=None,
		operation_id='ArticleRate',
		tags=['Article'],
	)
	def post(self, request, *args, **kwargs):
		try:
			article_obj = Article.objects.get(id=kwargs.get('article_id'))
		except Article.DoesNotExist:
			return error_response(
				error=ErrorObject.ARTICLE_NOT_FOUND,
				status_code=status.HTTP_404_NOT_FOUND,
			)

		serializer = self.serializer_class(data=request.data)
		if not serializer.is_valid():
			return self.serializer_error_response(serializer)

		ArticleRate.check_score_and_save(
			article=article_obj,
			user=request.user,
			score=serializer.validated_data.get('rate'),
		)

		return success_response(None, status_code=status.HTTP_201_CREATED)