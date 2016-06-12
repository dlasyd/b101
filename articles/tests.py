from django.test import TestCase
from .models import Article


class ArticleModelTest(TestCase):
    def test_create_article(self):
        article = Article()
        article.title = 'This is a test article'
        article.text = '<p>Full text of article, containing html</p>'
        article.save()

        self.assertEqual(1, Article.objects.count())


class ArticleTest(TestCase):
    def setUp(self):
        Article.objects.create(title='first title', text='low carb diet helps weight loss')
        Article.objects.create(title='Second title', text='second article text, more interesting')
        self.response = self.client.get('/')
        self.single_article = self.client.get('/article/1')

    def test_front_page_has_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'articles/article-list.html')

    def test_article_list_view_contains_article_titles(self):
        self.assertEqual(self.response.context['articles'][0], Article.objects.all()[0])
        # self.assertListEqual(self.response.context['articles'], Article.objects.all())

    def test_single_page_view_exists(self):
        self.assertEqual(self.single_article.status_code, 200)

    def test_single_page_render_with_correct_template(self):
        self.assertTemplateUsed(self.single_article, 'articles/single-article.html')

    def test_single_page_contains_article(self):
        self.assertEquals(Article.objects.get(id=1), self.single_article.context['article'])

    def test_single_page_view_id_url(self):
        r = self.client.get('/article/2')
        self.assertEqual(r.status_code, 200)
        self.assertEquals(Article.objects.get(id=2), r.context['article'])
