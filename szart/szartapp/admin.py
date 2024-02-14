from django.contrib import admin
from .models import Product, Like, Cart, CartItem, Order, OrderItem, Message

admin.site.register(Product)
admin.site.register(Like)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Message)