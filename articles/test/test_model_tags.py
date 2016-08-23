from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from articles.models import Article, Tag, Category


class TagModelTest(TestCase):

    def test_can_create_tag(self):
        Tag.objects.create(name='вендинг')
        self.assertEqual('вендинг', Tag.objects.first().name)

    def test_article_can_have_several_tags(self):
        Category.objects.create(name="разное")
        self.cat1 = Category.objects.first()
        User.objects.create()
        self.u1 = User.objects.first()
        tag1 = Tag()
        tag1.name = 'стартовый капитал'
        tag1.save()
        tag2 = Tag()
        tag2.name = 'инвестиции'
        tag2.save()
        Article.objects.create(title='Статья для теста',
                               text='<p>Full text of article, containing html</p>',
                               preview_text='This is preview text',
                               author=self.u1,
                               creation_date=timezone.now(),
                               category=self.cat1,
                               )
        self.article = Article.objects.last()
        self.article.tags.add(tag1)
        self.article.tags.add(tag2)
        self.assertEqual(self.article.tags.get(pk=tag1.pk), tag1)
        self.assertEqual(self.article.tags.get(pk=tag2.pk), tag2)

    def test_tag_name_should_be_unique(self):
        Tag.objects.create(name="investing")
        with self.assertRaises(IntegrityError):
            Tag.objects.create(name="investing")

