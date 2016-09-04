from django.test import TestCase
from articles.models import Category
from django.db import IntegrityError


class CategoryTest(TestCase):
    def test_category_has_name_and_alias(self):
        Category.objects.create(
            name="Разное"
        )
        self.assertEqual(Category.objects.first().slug, "raznoe")

    def test_can_set_category_alias(self):
        category = Category.objects.create(name='hello', slug='world')
        self.assertEqual(category.slug, 'world')

    def test_category_name_should_be_unique(self):
        Category.objects.create(name='Идеи бизнеса', slug='world')
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Идеи бизнеса')

    def test_category_alias_should_be_unique(self):
        Category.objects.create(name='Идеи бизнеса', slug='world')
        with self.assertRaises(IntegrityError):
            Category.objects.create(name='Investing', slug='world')

    def test_no_category_without_name(self):
        with self.assertRaises(IntegrityError):
            Category.objects.create(slug='123')

