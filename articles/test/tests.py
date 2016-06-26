import datetime

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from articles.models import Article


class ArticleModelTest(TestCase):
    def test_create_article(self):

        author1 = User('john', 'lennon@thebeatles.com', 'johnpassword')
        User.objects.create()
        u1 = User.objects.first()

        Article.objects.create(title='Статья для теста',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=u1,
                               creation_date=datetime.datetime.now(),
                               # main_image='?other table',
                               # category='?other table',
                               # url_alias='?other table',
                               # tags='?other table legacy tags'
                               )

        article = Article.objects.first()
        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            article.teaser_image.save('test_teaser.jpg', File(image), save=True)

        self.assertEqual(1, Article.objects.count())
        self.assertIsNotNone(article.creation_date)
        self.assertFalse(article.is_published)
        # self.assertEqual(article.url_alias, 'staia-dlya-testa')