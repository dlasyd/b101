"""b111 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from articles.views import legacy_redirect, ArticleDetailed, CategoryList, AllArticlesList

urlpatterns = [
    url(r'^editor/', admin.site.urls),
    url(r'^$', AllArticlesList.as_view(), name='article-list'),
    url(r'^articles/(?P<page>[\d]+)$', AllArticlesList.as_view(), name='article-list-archive'),
    url(r'^lenta/(?P<slug>[-\w]+)$', legacy_redirect, name='legacy-redirect'),
    url(r'^article/(?P<slug>[-\w]+)$', ArticleDetailed.as_view(), name='article-view'),
    url(r'^topic/(?P<slug>[-\w]+)$', CategoryList.as_view(), name='category'),
    url(r'^topic/(?P<slug>[-\w]+)/(?P<page>[\d]+)$', CategoryList.as_view(), name='category')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Управление сайтом Business101.ru"
