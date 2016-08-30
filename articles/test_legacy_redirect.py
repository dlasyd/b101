from django.test import TestCase
from django.contrib.auth.models import User
from articles.models import Article, Category


class LentaTest(TestCase):
    def setUp(self):
        User.objects.create()
        nata = User.objects.first()
        Category.objects.create(name='Бизнес в Твери')
        cat = Category.objects.first()

        Article.objects.create(title='modern-article',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               category=cat)

        Article.objects.create(title='legacy-article',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               category=cat,
                               legacy=True,
                               state='3')

    def test_redirect_on_lenta_url_to_article(self):
        response = self.client.get('/lenta/legacy-article')
        self.assertRedirects(response,
                             expected_url='/article/legacy-article',
                             status_code=301,
                             target_status_code=200)

    def test_no_redirect_if_article_does_not_exist(self):
        response = self.client.get('/lenta/modern-article')
        self.assertEqual(response.status_code, 404)


