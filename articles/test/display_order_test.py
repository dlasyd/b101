from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from articles.models import Article, Category


class DisplayOrderTest(TestCase):

    def setUp(self):
        User.objects.create()
        self.nata = User.objects.first()

        Category.objects.create(name='идеи бизнеса')
        self.cat = Category.objects.first()

        Article.objects.create(title='should be second',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.nata,
                               category=self.cat,
                               state='3',
                               published_date=timezone.now())

        Article.objects.create(title='should be first',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.nata,
                               category=self.cat,
                               state='3',
                               published_date=timezone.now())

        Article.objects.create(title='should be third',
                               text='low carb diet helps weight loss',
                               preview_text='eat less',
                               author=self.nata,
                               category=self.cat,
                               state='3',
                               published_date=timezone.now())

    def test_correct_order(self):
        self.fail()

