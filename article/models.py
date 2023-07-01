from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class Article(models.Model):
	title = models.CharField(_("title"), max_length=100)
	content = models.TextField(_("content"))

	class Meta:
		verbose_name = _("article")
		verbose_name_plural = _("articles")
		unique_together = ("title", "content")

	def __str__(self):
		return self.title


class ArticleRate(models.Model):
	article = models.ForeignKey(
		Article,
		on_delete=models.CASCADE,
		related_name="article_rates",
		verbose_name=_("article"),
	)
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="user_rates",
		verbose_name=_("user"),
	)
	rate = models.SmallIntegerField(_("rate"), default=0)

	def __str__(self):
		return f"{self.article.title} - {self.user.email}"

	@staticmethod
	def check_score_and_save(article, user, score):
		"""
		if a user has already rated this article, update the rate
		else create a new rate.
		"""
		article_rate = ArticleRate.objects.filter(
			article=article,
			user=user,
		).first()
		if article_rate:
			article_rate.rate = score
			article_rate.save()
		else:
			ArticleRate.objects.create(
				article=article,
				user=user,
				rate=score,
			)
