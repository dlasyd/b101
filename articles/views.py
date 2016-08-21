from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Article, Category
from django.http import Http404


def article_list(request):
    articles = get_list_or_404(Article.objects.all())
    return render(request, 'articles/article-list.html', {'articles': articles})


def single_article(request, url_alias):
    article = get_object_or_404(Article, url_alias=url_alias)
    return render(request, 'articles/single-article.html', {'article': article})


def legacy_redirect(request, legacy_url):
    article = get_object_or_404(Article, url_alias=legacy_url)
    if article.legacy:
        return redirect('article-view', url_alias=legacy_url, permanent=True)
    else:
        raise Http404("Article does not exist")


def category(request, category):
    cat = get_object_or_404(Category, url_alias=category)
    articles = get_list_or_404(Article.objects.filter(category=cat))
    return render(request, 'articles/category.html', {'category': cat, 'articles': articles})
