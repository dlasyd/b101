import os

from django.core.files import File
from django.contrib.auth.models import User
from django.test import TestCase

from articles.models import Article, Category


class ArticleTest(TestCase):
    def setUp(self):
        User.objects.create()
        nata = User.objects.first()

        Category.objects.create(name='идеи бизнеса')
        cat = Category.objects.first()

        Article.objects.create(title='first title',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=nata,
                               category=cat)
        self.firstArticle = Article.objects.last()

        Article.objects.create(title='Второе название',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               category=cat,
                               legacy=True)
        self.secondArticle = Article.objects.last()

        self.response = self.client.get('/')
        self.single_article = self.client.get('/article/first-title')

    def test_front_page_has_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'articles/all-articles-list.html')

    def test_article_list_view_contains_article_preview(self):
        article = Article.objects.first()
        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            article.teaser_image.save('test_teaser.jpg', File(image), save=True)
        self.response = self.client.get('/')

        self.assertContains(self.response, Article.objects.first().teaser_image.url)
        self.assertContains(self.response, Article.objects.first().preview_text)

        if os.path.isfile(article.teaser_image.path):
            os.remove(article.teaser_image.path)

    def test_single_page_view_exists(self):
        self.assertEqual(self.single_article.status_code, 200)

    def test_single_page_render_with_correct_template(self):
        self.assertTemplateUsed(self.single_article, 'articles/article-detailed.html')

    def test_single_page_contains_article(self):
        self.assertEquals(self.firstArticle, self.single_article.context['article'])

    def test_single_page_view_id_url(self):
        r = self.client.get('/article/vtoroe-nazvanie')
        self.assertEqual(r.status_code, 200)
        self.assertEquals(self.secondArticle, r.context['article'])

    def test_redirect_on_lenta_url_to_article(self):

        response = self.client.get('/lenta/vtoroe-nazvanie')
        self.assertRedirects(response,
                             expected_url='/article/vtoroe-nazvanie',
                             status_code=301,
                             target_status_code=200)

    def test_no_redirect_if_article_does_not_exist(self):
        response = self.client.get('/article/first-title')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/lenta/first-title')
        self.assertEqual(response.status_code, 404)

    def test_category_has_url_address(self):
        r = self.client.get('/topic/idei-biznesa')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Идеи бизнеса')
        self.assertContains(r, self.firstArticle.title)

    def test_category_has_correct_template(self):
        r = self.client.get('/topic/idei-biznesa')
        self.assertTemplateUsed(r, 'articles/articles-by-category-list.html')

