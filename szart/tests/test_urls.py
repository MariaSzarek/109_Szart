from django.test import TestCase
from django.urls import resolve
from django.test.client import RequestFactory

from szartapp import views


class UrlTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_szart_url(self):
        url = resolve('/szart/')
        self.assertEqual(url.func, views.index)
        self.assertEqual(url.url_name, 'szart')

    def test_ceramika_url(self):
        url = resolve('/ceramika/')
        self.assertEqual(url.func, views.show_ceramics)
        self.assertEqual(url.url_name, 'ceramika')

    def test_ceramika_url(self):
        url = resolve('/malarstwo/')
        self.assertEqual(url.func, views.show_paintings)
        self.assertEqual(url.url_name, 'malarstwo')

    def test_kontakt_url(self):
        url = resolve('/kontakt/')
        self.assertEqual(url.func, views.contact_response)
        self.assertEqual(url.url_name, 'kontakt')

    def test_item_url(self):
        url = resolve('/item/1')
        self.assertEqual(url.func, views.item_response)
        self.assertEqual(url.url_name, 'item')

    def test_add_to_fav_url(self):
        url = resolve('/add_to_fav/1/')
        self.assertEqual(url.func, views.add_to_fav)
        self.assertEqual(url.url_name, 'add_to_fav')

    def test_add_to_cart_url(self):
        url = resolve('/add_to_cart/1/')
        self.assertEqual(url.func, views.add_to_cart)
        self.assertEqual(url.url_name, 'add_to_cart')

    def test_del_from_cart_url(self):
        url = resolve('/del_from_cart/1/')
        self.assertEqual(url.func, views.del_from_cart)
        self.assertEqual(url.url_name, 'del_from_cart')

    def test_ulubione_url(self):
        url = resolve('/ulubione/')
        self.assertEqual(url.func, views.favorite_response)
        self.assertEqual(url.url_name, 'favorite')


    def test_koszyk_url(self):
        url = resolve('/koszyk/')
        self.assertEqual(url.func, views.cart)
        self.assertEqual(url.url_name, 'cart')

    def test_zamowienie_url(self):
        url = resolve('/zamowienie/')
        self.assertEqual(url.func, views.place_order)
        self.assertEqual(url.url_name, 'zamowienie')