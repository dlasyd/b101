from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
import json

from .models import Article, Category


class PaginatorMixin:
    def select_paginated(self, articles, **kwargs):
        paginator = Paginator(articles, self.paginate_by)

        try:
            articles = paginator.page(self.kwargs['page'])
        except KeyError:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        return articles


class ArticleDetailed(DetailView):
    model = Article
    template_name = 'articles/article-detailed.html'

    def get_queryset(self):
        return Article.objects.published()


class CategoryList(ListView):
    template_name = 'articles/articles-by-category-list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.cat = get_object_or_404(Category, slug=self.kwargs['slug'])
        return get_list_or_404(Article.objects.filter(category=self.cat, state='3'))

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['category'] = self.cat
        articles = Article.objects.published_in_category(category=self.cat)
        paginator = Paginator(articles, self.paginate_by)

        try:
            articles = paginator.page(self.kwargs['page'])
        except KeyError:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        return context


class AllArticlesList(ListView, PaginatorMixin):
    model = Article
    template_name = 'articles/all-articles-list.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.published()

    def get_context_data(self, **kwargs):
        context = super(AllArticlesList, self).get_context_data(**kwargs)
        articles = Article.objects.published()
        paginator = Paginator(articles, self.paginate_by)


        try:
            articles = paginator.page(self.kwargs['page'])
        except KeyError:
            articles = paginator.page(1)
        except EmptyPage:
            articles = paginator.page(paginator.num_pages)

        context['articles'] = articles
        return context


def legacy_redirect(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.legacy:
        return redirect('article-view', slug=slug, permanent=True)
    else:
        raise Http404("Article does not exist")
