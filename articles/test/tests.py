import os

from django.core.files import File
from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Category


class ArticleTest(TestCase):
    def setUp(self):
        User.objects.create()
        nata = User.objects.first()

        Category.objects.create(name='Бизнес в Твери')
        cat = Category.objects.first()

        Article.objects.create(title='first title',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=nata,
                               category=cat)
        Article.objects.create(title='Второе название',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               is_published=True,
                               category=cat)
        self.response = self.client.get('/')
        self.single_article = self.client.get('/article/first-title')

    def test_front_page_has_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'articles/article-list.html')

    def test_article_list_view_contains_article_preview(self):
        article = Article.objects.first()
        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            article.teaser_image.save('test_teaser.jpg', File(image), save=True)
        self.response = self.client.get('/')

        self.assertEqual(self.response.context['articles'][0], Article.objects.all()[0])
        self.assertContains(self.response, Article.objects.first().teaser_image.url)
        self.assertContains(self.response, Article.objects.first().preview_text)
        # self.assertListEqual(self.response.context['articles'], Article.objects.all())

        if os.path.isfile(article.teaser_image.path):
            os.remove(article.teaser_image.path)

    def test_single_page_view_exists(self):
        self.assertEqual(self.single_article.status_code, 200)

    def test_single_page_render_with_correct_template(self):
        self.assertTemplateUsed(self.single_article, 'articles/single-article.html')

    def test_single_page_contains_article(self):
        self.assertEquals(Article.objects.get(id=1), self.single_article.context['article'])

    def test_single_page_view_id_url(self):
        r = self.client.get('/article/vtoroe-nazvanie')
        self.assertEqual(r.status_code, 200)
        self.assertEquals(Article.objects.get(id=2), r.context['article'])

    def test_legacy_article_redirects_to_new(self):
        pass
