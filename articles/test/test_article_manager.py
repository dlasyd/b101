from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
import datetime

from articles.models import Article, Category


class ArticleModelManagerTest(TestCase):
    def setUp(self):
        Category.objects.create(name="разное")
        self.cat1 = Category.objects.first()
        Category.objects.create(name="tested category")
        self.tested_category = Category.objects.last()
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

        Article.objects.create(title='should be fourth',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1,
                               state='3',
                               published_date=timezone.now()-datetime.timedelta(days=3))

        Article.objects.create(title='should be second',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.u1,
                               category=self.cat1,
                               state='3',
                               published_date=timezone.now() - datetime.timedelta(days=1))

        Article.objects.create(title='should be first',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.u1,
                               category=self.cat1,
                               state='3',
                               published_date=timezone.now())

        Article.objects.create(title='should be third',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.u1,
                               category=self.cat1,
                               state='3',
                               published_date=timezone.now() - datetime.timedelta(days=2))

        Article.objects.create(title='article in tested category',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.u1,
                               category=self.tested_category,
                               state='3',
                               published_date=timezone.now() - datetime.timedelta(days=20)
                               )

    def test_only_published_articles_are_displayed_in_correct_order(self):
        articles = Article.objects.published()
        self.assertEqual(len(articles), 5)
        self.assertEqual('should be first', articles[0].title)
        self.assertEqual('should be second', articles[1].title)
        self.assertEqual('should be third', articles[2].title)
        self.assertEqual('should be fourth', articles[3].title)

    def test_get_by_category(self):
        articles = Article.objects.published_in_category(self.tested_category)
        self.assertEqual(1, len(articles))
        self.assertEqual('article in tested category', articles[0].title)
