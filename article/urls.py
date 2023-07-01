from django.urls import include, path

app_name = 'article'

urlpatterns = [
    path('v1/', include('article.api.v1.urls')),
]
