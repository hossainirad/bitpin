from django.urls import path

from article.api.v1.views import ArticleListAPIView, ArticleRateAPIView

app_name = 'v1'

urlpatterns = [
	path('article/article-list/', ArticleListAPIView.as_view(), name='article_list'),
	path('article/<int:article_id>/rate/', ArticleRateAPIView.as_view(), name='article_rate'),
]
