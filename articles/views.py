from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Article


def article_list(request):
    articles = get_list_or_404(Article.objects.all())
    return render(request, 'articles/article-list.html', {'articles': articles})


def single_article(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'articles/single-article.html', {'article': article})
