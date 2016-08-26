import os

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
import datetime

from articles.models import Article, Category


class ArticleModelTest(TestCase):
    def setUp(self):
        Category.objects.create(name="разное")
        self.cat1 = Category.objects.first()
        User.objects.create()
        self.u1 = User.objects.first()

        Article.objects.create(title='Статья для теста',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )
        self.article = Article.objects.last()

    def test_create_article(self):

        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            self.article.teaser_image.save('test_teaser.jpg', File(image), save=True)

        self.assertIsNotNone(self.article.creation_date)
        self.assertFalse(self.article.is_published)
        self.assertEqual('statja-dlja-testa', self.article.url_alias)

        if os.path.isfile(self.article.teaser_image.path):
            os.remove(self.article.teaser_image.path)

    def test_create_without_date_and_image(self):
        Article.objects.create(title='Статья без даты и картинки',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )

        self.assertNotEqual(Article.objects.last().creation_date, None)

    def test_create_article_with_mixed_language_title(self):
        Article.objects.create(title='Статья для hello',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )

        article = Article.objects.last()
        self.assertEqual('statja-dlja-hello', article.url_alias)

    def test_alias_size_constrains(self):

        Article.objects.create(title='Очень очень приочень длинное придлинное название статьи для сайта',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               category=self.cat1
                               )

        article = Article.objects.last()
        self.assertEqual('ochen-ochen-priochen-dlinnoe-pridlinnoe-nazvanie-s', article.url_alias)

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

    def test_can_set_publish_date(self):
        Article.objects.create(title='Тест статьи с датой публикации',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1,
                               published_date=timezone.now()
                               )
        self.assertNotEqual(Article.objects.last(), None)

    def test_when_published_is_set_to_true_publication_is_now(self):
        self.article.is_published = True
        self.article.save()
        time_pub = self.article.published_date
        self.assertNotEqual(time_pub, None)

        self.article.is_published = False
        self.article.save()
        self.assertEqual(self.article.published_date, time_pub)

        self.article.is_published = True
        self.article.save()
        self.assertEqual(self.article.published_date, time_pub)

    def test_new_article_is_published_sets_publish_date(self):
        Article.objects.create(title='Опубликованная сразу статья',
                               is_published=True,
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1,
                               )

        self.assertNotEqual(Article.objects.last().published_date, None)

    def test_new_article_not_published_does_not_set_date(self):
        Article.objects.create(title='Не опубликованная сразу статья',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1,
                               )

        self.assertEqual(Article.objects.last().published_date, None)

    def test_new_article_is_published_with_set_publish_date_does_not_override_date(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)

        Article.objects.create(title='Опубликованная статья с датой публикации',
                               is_published=True,
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1,
                               published_date=yesterday
                               )

        self.assertEqual(Article.objects.last().published_date, yesterday)
