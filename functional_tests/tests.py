from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from articles.models import Article
import time


class FunctionalTests(StaticLiveServerTestCase):
    def setUp(self):
        self.article1 = Article()
        self.article1.title = 'Start your own wending business'
        self.article1.text = 'Wending machines are easy to maintain and they will make a lot of money'
        self.article1.save()

        self.article2 = Article()
        self.article2.title = 'Start up money'
        self.article2.text = 'Where to get them'
        self.article2.save()

        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.close()

    def test_user_can_read_article(self):
        self.browser.get(self.live_server_url)
        # user clicks on first article title
        self.browser.find_element_by_link_text(self.article1.title).click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/article/1')

        assert self.article1.title in self.browser.title
        assert self.article1.text in self.browser.page_source

        self.browser.execute_script("window.history.go(-1)")

        self.browser.find_element_by_link_text(self.article2.title).click()
        self.assertEqual(self.browser.current_url, self.live_server_url + '/article/2')

        assert self.article2.title in self.browser.title
        assert self.article2.text in self.browser.page_source




