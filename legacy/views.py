from django.shortcuts import redirect, get_object_or_404
from articles.models import Article
from django.http import Http404


def legacy_redirect(request, legacy_url):
    article = get_object_or_404(Article, url_alias=legacy_url)
    if article.legacy:
        return redirect('article-view', url_alias=legacy_url, permanent=True)
    else:
        raise Http404("Article does not exist")
