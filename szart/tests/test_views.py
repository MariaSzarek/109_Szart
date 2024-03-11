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
        self.post = Product.objects.create(title='Product1', short_desc='This is a short desc', price=1200.00)

    def test_index(self):
        with CaptureQueriesContext(connection) as ctx:
            response = self.client.get('index')
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'Szart.html')

            # # Check the SQL query generated
            # expected_query = (
            #     f"""SELECT "blog_post"."id", "blog_post"."author_id", "blog_post"."title",
            #     "blog_post"."text", "blog_post"."created_date", "blog_post"."published_date"
            #     FROM "blog_post"
            #     WHERE "blog_post"."published_date" <= \'2024-03-05 08:05:21.118404\'
            #     ORDER BY "blog_post"."published_date" ASC """
            # ).replace("\n", "").replace(" ", "")
            #
            # actual_query = ctx.captured_queries[0]['sql'].replace("\n", "").replace(" ", "")
            # self.assertEqual(expected_query, actual_query)