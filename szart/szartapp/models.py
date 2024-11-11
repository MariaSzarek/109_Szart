from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    TYPE = {
        (0, 'Malarstwo'),
        (1, 'Ceramika'),
    }

    SOLD = {
        (0, 'Kup'),
        (1, 'Zapytaj o podobne')
    }

    title = models.CharField(max_length=64, blank=False, unique=True)
    year = models.PositiveSmallIntegerField(null=True, blank=True)
    short_desc = models.CharField(max_length=128, blank=False, default='')
    description = models.TextField(default="")
    image = models.ImageField(upload_to="images", null=False, blank=False, default='')
    type = models.PositiveSmallIntegerField(default=0, choices=TYPE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    sold = models.PositiveSmallIntegerField(default=0, choices=SOLD)

    def __str__(self):
        return f"{self.id} {self.title} {self.price}"

    def mark_as_sold(self):
        self.sold = 1
        self.save()

class Like(models.Model):
    CHOICES = {
        (0, 'niepolubione'),
        (1, 'polubione')
    }

    like = models.PositiveSmallIntegerField(default=0, choices=CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return f" {self.product.title} {self.like} {self.user}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f" {self.user} {self.total_price} "

    def update_total_price(self):
        total_price = sum(item.price for item in self.items.all())
        self.total_price = total_price
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f" {self.cart} {self.product.title} "


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='OrderItem')
    delivery_address = models.CharField(max_length=200)

    total_price = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def place_order(self):
        for order_item in self.order_items.all():
            order_item.product.mark_as_sold()

    def get_ordered_products(self):
        ordered_products = self.items.all()
        return ordered_products

    def update_total_price(self):
        total_price = sum(item.price for item in self.items.all())
        self.total_price = total_price
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order: {self.order.id}, Product: {self.product.title}"


class Message(models.Model):
    nadawca = models.CharField(max_length=100)
    email = models.EmailField()
    temat = models.CharField(max_length=200)
    tresc = models.TextField()

    def __str__(self):
        return f" {self.nadawca} {self.temat} "