from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.detail import DetailView

from .models import Article, Category


class ArticleDetailed(DetailView):
    model = Article
    template_name = 'articles/single-article.html'
    slug_field = 'url_alias'


def article_list(request):
    articles = get_list_or_404(Article.objects.all())
    return render(request, 'articles/article-list.html', {'articles': articles})


def single_article(request, url_alias):
    article = get_object_or_404(Article, url_alias=url_alias)
    return render(request, 'articles/single-article.html', {'article': article})


def legacy_redirect(request, legacy_url):
    article = get_object_or_404(Article, url_alias=legacy_url)
    if article.legacy:
        return redirect('article-view', slug=legacy_url, permanent=True)
    else:
        raise Http404("Article does not exist")


def category(request, category):
    cat = get_object_or_404(Category, url_alias=category)
    articles = get_list_or_404(Article.objects.filter(category=cat))
    return render(request, 'articles/category.html', {'category': cat, 'articles': articles})
