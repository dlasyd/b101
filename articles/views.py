from django.shortcuts import get_list_or_404, get_object_or_404, redirect
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Article, Category


class ArticleDetailed(DetailView):
    model = Article
    template_name = 'articles/article-detailed.html'


class CategoryList(ListView):
    template_name = 'articles/articles-by-category-list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        self.cat = get_object_or_404(Category, slug=self.kwargs['slug'])
        return get_list_or_404(Article.objects.filter(category=self.cat))

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        context['category'] = self.cat
        return context


class AllArticlesList(ListView):
    model = Article
    template_name = 'articles/all-articles-list.html'
    context_object_name = 'articles'


def legacy_redirect(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if article.legacy:
        return redirect('article-view', slug=slug, permanent=True)
    else:
        raise Http404("Article does not exist")
