from django.db import models


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(state='3').order_by('-published_date')

    def published_in_category(self, category):
        articles = self.filter(state='3', category=category).order_by('published_date')
        return articles
