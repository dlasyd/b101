from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from articles.models import Article, Category
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone
import os


class FunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create()
        u1 = User.objects.first()

        Category.objects.create(name='Какой бизнес открыть')
        self.cat1 = Category.objects.first()

        Category.objects.create(name='разное')
        self.cat2 = Category.objects.last()

        self.article1 = Article()
        self.article1.title = 'Начни свой бизнес в сфере вендинга'
        self.article1.text = 'Wending machines are easy to maintain and they will make a lot of money'
        self.article1.preview_text = 'This is preview text'
        self.article1.author = u1
        self.article1.category = self.cat1
        self.article1.creation_date = timezone.now()
        self.article1.state = '3'
        self.article1.save()

        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            self.article1.teaser_image.save('test_teaser.jpg', File(image), save=True)

        self.article2 = Article()
        self.article2.title = 'Start up money'
        self.article2.text = 'Where to get them'
        self.article2.preview_text = 'This is preview text'
        self.article2.author = u1
        self.article2.category = self.cat1
        self.article2.creation_date = timezone.now()
        self.article2.state = '3'
        self.article2.save()

        # why doesn't article.objects.create work here?
        legacy_article = Article()
        legacy_article.title = 'Legacy article example'
        legacy_article.text = 'Used to have lenta in url. Where to get them'
        legacy_article.preview_text = 'This very legacy'
        legacy_article.author = u1
        legacy_article.category = self.cat2
        legacy_article.creation_date = timezone.now()
        legacy_article.legacy = True
        legacy_article.save()

        self.browser = webdriver.Firefox()
        self.homepage = self.live_server_url

    def tearDown(self):
        if os.path.isfile(self.article1.teaser_image.path):
            os.remove(self.article1.teaser_image.path)
        self.browser.close()

    def test_user_can_read_article(self):
        self.browser.get(self.live_server_url)

        assert self.article1.preview_text in self.browser.page_source
        assert self.article1.teaser_image.url in self.browser.page_source
        # user clicks on first article title
        self.browser.find_element_by_link_text(self.article1.title).click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/article/nachni-svoj-biznes-v-sfere-vendinga')

        assert self.article1.title in self.browser.title
        assert self.article1.text in self.browser.page_source

        self.browser.execute_script("window.history.go(-1)")

        self.browser.find_element_by_link_text(self.article2.title).click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/article/start-up-money')

        assert self.article2.title in self.browser.title
        assert self.article2.text in self.browser.page_source

    def test_logo_in_top_left_is_a_link(self):
        self.browser.get(self.homepage + '/article/nachni-svoj-biznes-v-sfere-vendinga')
        self.browser.find_element_by_id("logo").click()

        self.assertEquals(self.homepage + '/', self.browser.current_url)

    def test_legacy_article_redirects_to_correct_article(self):
        self.browser.get(self.homepage + '/lenta/legacy-article-example')
        expected_url = self.homepage + '/article/legacy-article-example'
        self.assertEqual(expected_url, self.browser.current_url)

    def test_category_has_address(self):
        self.browser.get(self.homepage + '/topic/kakoj-biznes-otkryt')
        actual_title = self.browser.title
        self.assertEqual(actual_title, 'Какой бизнес открыть')

    def test_article_has_link_to_category(self):
        self.browser.get(self.homepage + '/article/nachni-svoj-biznes-v-sfere-vendinga')
        self.browser.find_element_by_link_text('Какой бизнес открыть').click()
        self.assertEquals(self.homepage + '/topic/kakoj-biznes-otkryt', self.browser.current_url)

    def test_category_page_displays_correct_articles(self):
        self.browser.get(self.homepage + '/topic/raznoe')
        self.browser.find_element_by_link_text('Legacy article example').click()
        self.assertEqual(self.browser.current_url, self.homepage + '/article/legacy-article-example')

        self.browser.get(self.homepage + '/topic/kakoj-biznes-otkryt')
        self.browser.find_element_by_link_text('Начни свой бизнес в сфере вендинга').click()
        self.assertEqual(self.browser.current_url, self.homepage + '/article/nachni-svoj-biznes-v-sfere-vendinga')


