# __init__.py
# models/
#     __init__.py
#     foo.py
#     bar.py
# views/
#     __init__.py
#     foo.py
#     bar.py
# forms/
#     __init__.py
#     foo.py
#     bar.py
# tests/
#     __init__.py
#     test_foo_models.py
#     test_bar_models.py
#     test_foo_views.py
#     test_bar_views.py
#     test_foo_forms.py
#     test_bar_forms.py

from django.test import TestCase

from django.contrib.auth.models import User
from blog.models import Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Product.objects.create(
            title='Title',
            short_desc='Kiciuś Cat ipsum',
            author=test_user
        )

    def test_title_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_short_desc_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('short_desc').verbose_name
        self.assertEqual(field_label, 'short_desc')

    def test_title_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)

    def test_object_name_is_title(self):
        product = Product.objects.get(id=1)
        expected_object_name = product.title
        self.assertEqual(str(product), expected_object_name)

    def test_mark_as_sold(self):
        product = Product.objects.get(id=1)
        self.assertFalse(product.sold)
        product.mark_as_sold()
        self.assertTrue(product.sold)

