from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Article


def article_list(request):
    articles = get_list_or_404(Article.objects.all())
    return render(request, 'articles/article-list.html', {'articles': articles})


def single_article(request, url_alias):
    article = get_object_or_404(Article, url_alias=url_alias)
    return render(request, 'articles/single-article.html', {'article': article})
