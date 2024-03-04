from django.test import TestCase
from django.contrib.auth.models import User
from szartapp.models import Product, Like

class LikeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(username='testuser', password='12345')
        test_product = Product.objects.create(
            title='Title',
            short_desc='Kiciuś Cat ipsum',
            price=1200.00)
        Like.objects.create(
            like=0,
            product= test_product,
            user=test_user)

    def test_like_label(self):
        like = Like.objects.get(id=1)
        field_label = like._meta.get_field('like').verbose_name
        self.assertEqual(field_label, 'like')

    def test_like_choices(self):
        like = Like.objects.get(id=1)
        choices = like._meta.get_field('like').choices
        self.assertEqual(choices, Like.CHOICES)

    def test_product_label(self):
        like = Like.objects.get(id=1)
        field_label = like._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'product')

    def test_product_foreignkey(self):
        like = Like.objects.get(id=1)
        self.assertIsInstance(like.product, Product)

    def test_product_ondelete(self):
        like = Like.objects.get(id=1)
        test_product = like.product
        self.assertTrue(Like.objects.filter(pk=like.pk).exists())
        self.assertTrue(Product.objects.filter(pk=test_product.pk).exists())
        test_product.delete()
        self.assertFalse(Like.objects.filter(pk=like.pk).exists())
        self.assertFalse(Product.objects.filter(pk=test_product.pk).exists())

    # def test_product_ondelete(self):
    #     like = Like.objects.get(id=1)
    #     on_delete = like._meta.get_field('product').on_delete
    #     self.assertEqual(on_delete, models.CASCADE)

    def test_product_default(self):
        like = Like.objects.get(id=1)
        default = like._meta.get_field('product').default
        self.assertEqual(default, '')

    def test_user_label(self):
        like = Like.objects.get(id=1)
        field_label = like._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_user_foreignkey(self):
        like = Like.objects.get(id=1)
        self.assertIsInstance(like.user, User)

    #def test_user_ondelete(self):

    def test_user_null(self):
        like = Like.objects.get(id=1)
        null = like._meta.get_field('user').null
        self.assertTrue(null)

    def test_user_blank(self):
        like = Like.objects.get(id=1)
        blank = like._meta.get_field('user').blank
        self.assertTrue(blank)


    def test_object_name(self):
        like = Like.objects.get(id=1)
        expected_object_name = f" {like.product.title} {like.like} {like.user}"
        self.assertEqual(str(like), expected_object_name)