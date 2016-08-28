from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article, Category


class ArticleDetailed(DetailView):
    model = Article
    template_name = 'articles/single-article.html'
    slug_field = 'url_alias'


class CategoryList(ListView):
    model = Category
    template_name = 'articles/category.html'

    def get_queryset(self):
        self.cat = get_object_or_404(Category, url_alias=self.kwargs['slug'])
        return get_list_or_404(Article.objects.filter(category=self.cat))

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['category'] = self.cat
        return context


def article_list(request):
    articles = get_list_or_404(Article.objects.all())
    return render(request, 'articles/article-list.html', {'object_list': articles})


def legacy_redirect(request, legacy_url):
    article = get_object_or_404(Article, url_alias=legacy_url)
    if article.legacy:
        return redirect('article-view', slug=legacy_url, permanent=True)
    else:
        raise Http404("Article does not exist")

