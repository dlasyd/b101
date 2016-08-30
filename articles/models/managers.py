from django.db import models


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(state='3')
