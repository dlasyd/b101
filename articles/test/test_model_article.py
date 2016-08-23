import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from articles.models import Article, Category


class ArticleModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name="разное")
        self.cat1 = Category.objects.first()
        User.objects.create()
        self.u1 = User.objects.first()

    def test_create_article(self):

        Article.objects.create(title='Статья для теста',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1
                               )

        article = Article.objects.first()
        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            article.teaser_image.save('test_teaser.jpg', File(image), save=True)

        self.assertEqual(1, Article.objects.count())
        self.assertIsNotNone(article.creation_date)
        self.assertFalse(article.is_published)
        self.assertEqual('statja-dlja-testa', article.url_alias)

        if os.path.isfile(article.teaser_image.path):
            os.remove(article.teaser_image.path)

    def test_create_without_date_and_image(self):
        Article.objects.create(title='Статья для теста',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )

        self.assertEqual(1, Article.objects.count())

    def test_create_article_with_mixed_language_title(self):
        Article.objects.create(title='Статья для hello',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )

        article = Article.objects.first()
        self.assertEqual('statja-dlja-hello', article.url_alias)

    def test_can_set_article_alias(self):
        article = Article()
        article.title = 'title'
        article.text = '<p> full text of the article <p>'
        article.preview_text = 'preview'
        article.author = self.u1
        article.category = self.cat1
        article.url_alias = 'custom-alias'
        article.save()

        self.assertEqual(article.url_alias, 'custom-alias')

    def test_alias_should_be_unique(self):
        a1 = Article()
        a1.title = 'title'
        a1.text = '<p> full text of the article <p>'
        a1.preview_text = 'preview'
        a1.author = self.u1
        a1.category = self.cat1
        a1.save()

        with self.assertRaises(IntegrityError):
            a2 = Article()
            a2.title = 'title'
            a2.text = '<p> full text of the article <p>'
            a2.preview_text = 'preview'
            a2.author = self.u1
            a2.category = self.cat1
            a2.save()




