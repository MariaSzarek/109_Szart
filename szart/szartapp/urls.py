from django.urls import path
from szartapp.views import index, item_response, show_paintings, show_ceramics, contact_response, add_to_fav, cart, add_to_cart, favorite_response, del_from_cart, place_order

urlpatterns = [
    path('szart/', index, name='szart'),
    path('ceramika/', show_ceramics, name='ceramika'),
    path('malarstwo/', show_paintings, name='malarstwo'),
    path('kontakt/', contact_response, name='kontakt'),
    path('item/<int:id>', item_response, name='item'),
    path('add_to_fav/<int:id>/', add_to_fav, name='add_to_fav'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    #path('del_from_fav/<int:id>/', del_from_fav, name='del_from_fav'),
    path('del_from_cart/<int:id>/', del_from_cart, name='del_from_cart'),
    path('ulubione/', favorite_response, name='favorite'),
    path('koszyk/', cart, name='cart'),
    path('zamowienie/', place_order, name='zamowienie')
]
