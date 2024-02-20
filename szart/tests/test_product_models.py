from django.test import TestCase

from django.contrib.auth.models import User
from szartapp.models import Product

class ProductModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        Product.objects.create(
            title='Title',
            short_desc='Kiciuś Cat ipsum',
            price=1200.00)

    def test_title_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_title_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('title').max_length
        self.assertEqual(max_length, 64)

    def test_title_blank(self):
        product = Product.objects.get(id=1)
        blank = product._meta.get_field('title').blank
        #self.assertEqual(blank, False)
        self.assertFalse(blank)

    def test_title_unique(self):
        product = Product.objects.get(id=1)
        unique = product._meta.get_field('title').unique
        self.assertTrue(unique)


    def test_short_desc_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('short_desc').verbose_name
        self.assertEqual(field_label, 'short desc')

    def test_short_desc_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('short_desc').max_length
        self.assertEqual(max_length, 128)

    def test_short_desc_blank(self):
        product = Product.objects.get(id=1)
        blank = product._meta.get_field('short_desc').blank
        self.assertFalse(blank)

    def test_short_desc_default(self):
        product = Product.objects.get(id=1)
        default = product._meta.get_field('short_desc').default
        self.assertEqual(default, '')

    def test_object_name(self):
        product = Product.objects.get(id=1)
        expected_object_name = f"{product.id} {product.title} {product.price}"
        self.assertEqual(str(product), expected_object_name)

    def test_mark_as_sold(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.sold, 0)
        product.mark_as_sold()
        self.assertEqual(product.sold, 1)

