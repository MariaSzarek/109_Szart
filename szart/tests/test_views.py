from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from freezegun import freeze_time

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import connection

from szartapp.models import Product
from szartapp.views import index

class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.product = Product.objects.create(title='Product1', short_desc='This is a short desc', price=1200.00)

    def test_index_nonauth(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('szart'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'Szart.html')



            expected_query = (
                f"""SELECT "szartapp_product"."id", "szartapp_product"."title", "szartapp_product"."year",
                "szartapp_product"."short_desc", "szartapp_product"."description", "szartapp_product"."image",
                "szartapp_product"."type", "szartapp_product"."price", "szartapp_product"."created",
                "szartapp_product"."sold"
                FROM "szartapp_product" """

            ).replace("\n", "").replace(" ", "")
            actual_query = ctx.captured_queries[0]['sql'].replace("\n", "").replace(" ", "")
            self.maxDiff = None
            self.assertEqual(expected_query, actual_query)

    def test_index_auth(self):
        self.client.force_login(self.user)
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get(reverse('szart'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'Szart.html')

            expected_query = (
                f"""SELECT "szartapp_product"."id", "szartapp_product"."title", "szartapp_product"."year", "szartapp_product"."short_desc",
                "szartapp_product"."description", "szartapp_product"."image", "szartapp_product"."type", "szartapp_product"."price",
                "szartapp_product"."created", "szartapp_product"."sold" 
                FROM "szartapp_product" 
                INNER JOIN "szartapp_like" ON ("szartapp_product"."id" = "szartapp_like"."product_id")
                WHERE ("szartapp_like"."like" = 1 
                AND "szartapp_like"."user_id" = 1)"""

            ).replace("\n", "").replace(" ", "")

            actual_query = ctx.captured_queries[3]['sql'].replace("\n", "").replace(" ", "")
            self.assertEqual(expected_query, actual_query)



    def test_item_response(self):
        response = self.client.get(reverse('item', kwargs={'id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'item.html')
