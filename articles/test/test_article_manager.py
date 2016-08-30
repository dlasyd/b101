from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Category


class ArticleModelManagerTest(TestCase):
    def setUp(self):
        Category.objects.create(name="разное")
        self.cat1 = Category.objects.first()
        User.objects.create()
        self.u1 = User.objects.first()

        Article.objects.create(title='Статья, которую только добавили',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1)

        Article.objects.create(title='Добавлена в автопубликацию',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1)

        Article.objects.create(title='Oпубликованая статья',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1,
                               state='3')

    def test_only_published_articles_are_displayed(self):
        articles = Article.objects.published()
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].title, 'Oпубликованая статья')
        pass

