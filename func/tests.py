from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from articles.models import Article
from django.contrib.auth.models import User
from django.core.files import File
from django.utils import timezone
import os


class FunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create()
        u1 = User.objects.first()

        self.article1 = Article()
        self.article1.title = 'Начни свой бизнес в сфере вендинга'
        self.article1.text = 'Wending machines are easy to maintain and they will make a lot of money'
        self.article1.preview_text = 'This is preview text'
        self.article1.author = u1
        self.article1.creation_date = timezone.now()
        self.article1.save()

        with open('articles/test/resources/test_teaser.jpg', 'rb') as image:
            self.article1.teaser_image.save('test_teaser.jpg', File(image), save=True)

        self.article2 = Article()
        self.article2.title = 'Start up money'
        self.article2.text = 'Where to get them'
        self.article2.preview_text = 'This is preview text'
        self.article2.author = u1
        self.article2.creation_date = timezone.now()
        self.article2.save()

        self.browser = webdriver.Firefox()

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

