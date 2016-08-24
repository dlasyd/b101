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
from articles.views import article_list, single_article, legacy_redirect, category

urlpatterns = [
    url(r'^editor/', admin.site.urls),
    url(r'^$', article_list, name='article-list'),
    url(r'^article/(?P<url_alias>[a-zA-Z0-9+-]+)$', single_article, name='article-view'),
    url(r'^lenta/(?P<legacy_url>[a-zA-Z0-9+-]+)$', legacy_redirect, name='legacy-redirect'),
    url(r'^topic/(?P<category>[a-zA-Z0-9+-]+)$', category, name='category')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Управление сайтом Business101.ru"
