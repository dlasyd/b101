from django.test import TestCase
from articles.models import Category


class CategoryTest(TestCase):
    def test_category_has_name_and_alias(self):
        Category.objects.create(
            name="Разное"
        )
        self.assertEqual(Category.objects.first().url_alias, "raznoe")
