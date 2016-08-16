from django.test import TestCase
from .models import Lenta
from django.contrib.auth.models import User
from articles.models import Article, Category


class LentaTest(TestCase):
    def setUp(self):
        self.legacy = Lenta()
        self.legacy.url = 'legacy-article'
        self.legacy.save()
        User.objects.create()
        nata = User.objects.first()
        Category.objects.create(name='Бизнес в Твери')
        cat = Category.objects.first()

        Article.objects.create(title='modern-article',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               is_published=True,
                               category=cat)

        Article.objects.create(title='legacy-article',
                               text='second article text, more interesting',
                               preview_text='interesting',
                               author=nata,
                               is_published=True,
                               category=cat,
                               legacy=True)

    def test_redirect_on_lenta_url_to_article(self):

        response = self.client.get('/lenta/legacy-article')
        self.assertRedirects(response,
                             expected_url='/article/legacy-article',
                             status_code=301,
                             target_status_code=200)


    def test_no_redirect_if_article_does_not_exist(self):
        response = self.client.get('/lenta/modern-article')
        self.assertEqual(response.status_code, 404)


    # def test_when_article_is_created_with_legacy_legacy_is_created(self):
    #     User.objects.create()
    #     nata = User.objects.first()
    #
    #     Category.objects.create(name='Бизнес в Твери')
    #     cat = Category.objects.first()
    #     Article.objects.create(title='Второе название',
    #                            text='second article text, more interesting',
    #                            preview_text='interesting',
    #                            author=nata,
    #                            is_published=True,
    #                            category=cat,
    #                            legacy=True)
    #
    #     obj = Lenta.objects.first()
    #     self.assertEquals(Article.objects.first().urt_alias, obj.url_alias)
