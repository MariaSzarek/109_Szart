from .models import Product, Like, Cart, CartItem, Order, OrderItem
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .forms import MessageForm

def index(request):
    products = Product.objects.all()
    liked_products = []
    user_authenticated = False

    if request.user.is_authenticated:
        liked_products = Product.objects.filter(like__like=1, like__user=request.user)
        user_authenticated = True

    return render(request, "Szart.html", {'items': products, 'liked_products': liked_products, 'added_to_cart': False, 'user_authenticated': user_authenticated})

def item_response(request, id):
    product = get_object_or_404(Product, pk=id)
    liked_products = []
    user_authenticated = False

    if request.user.is_authenticated:
        liked_products = Product.objects.filter(like__like=1, like__user=request.user)
        user_authenticated = True

    return render(request, 'item.html', {'item': product, 'liked_products': liked_products, 'added_to_cart': False, 'user_authenticated': user_authenticated})

def show_paintings(request):
    products = Product.objects.filter(type="0")
    liked_products = []
    user_authenticated = False

    if request.user.is_authenticated:
        liked_products = Product.objects.filter(like__like=1, like__user=request.user)
        user_authenticated = True

    return render(request, "paintings.html", {'items': products, 'liked_products': liked_products, 'added_to_cart': False, 'user_authenticated': user_authenticated})

def show_ceramics(request):
    products = Product.objects.filter(type="1")
    liked_products = []
    user_authenticated = False

    if request.user.is_authenticated:
        liked_products = Product.objects.filter(like__like=1, like__user=request.user)
        user_authenticated = True

    return render(request, "ceramics.html", {'items': products, 'liked_products': liked_products, 'added_to_cart': False, 'user_authenticated': user_authenticated})


def cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }
    return render(request, 'cart.html', context)


@login_required
def add_to_cart(request, id):
    if request.method == 'POST':
        added_item = None

        # Sprawdź, czy koszyk użytkownika już istnieje
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # Jeśli koszyk nie istnieje, utwórz nowy dla użytkownika
            cart = Cart.objects.create(user=request.user)

        product = Product.objects.get(pk=id)

        # Sprawdź, czy wybrany produkt znajduje się już w koszyku
        if CartItem.objects.filter(cart=cart, product=product).exists():
            #return HttpResponse("Ten produkt już znajduje się w koszyku.")
            messages.warning(request, 'Ten produkt już znajduje się w koszyku.')
            return redirect(request.META.get('HTTP_REFERER'))

        # Tworzenie nowego obiektu wybranego produktu i powiązanie go z koszykiem i produktem
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product)
            added_item = product

        cart.update_total_price()
        products = Product.objects.all()


        return render(request, "szart.html", {'items': products, 'added_to_cart': True, 'added_item_to_cart': added_item})

    #return redirect(request.META.get('HTTP_REFERER'))
    return redirect('szart')

@login_required
def del_from_cart(request, id):
    if request.method == 'POST':
        # Pobierz koszyk użytkownika
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            # Jeśli koszyk nie istnieje, zwróć odpowiedź z błędem lub przekieruj na inną stronę
            return HttpResponse("Koszyk nie istnieje.")

        product = Product.objects.get(pk=id)

            # Sprawdź, czy wybrany produkt znajduje się w koszyku
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
        except CartItem.DoesNotExist:
            # Jeśli produkt nie istnieje w koszyku, zwróć odpowiedź z błędem lub przekieruj na inną stronę
            return HttpResponse("Ten produkt nie znajduje się w koszyku.")

            # Usuń obiekt wybranego produktu z koszyka
        cart_item.delete()
        cart.update_total_price()

    return redirect('cart')


def place_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user, delivery_address='Adres dostawy')

    for cart_item in cart.items.all():
        order_item = OrderItem.objects.create(order=order, product=cart_item)
        cart_item.mark_as_sold()

    ordered_products = order.get_ordered_products()
    order.update_total_price()  # Aktualizuj total_price dla zamówienia
    total_price = order.total_price  # Pobierz zaktualizowaną wartość total_price

    context = {
        'ordered_products': ordered_products,
        'total_price': total_price
    }
    cart.items.clear()  # Usunięcie produktów z koszyka po złożeniu zamówienia
    cart.update_total_price()  # Aktualizacja ceny koszyka

    return render(request, 'order.html', context)

@login_required
def favorite_response(request):
    ulubione_produkty = Product.objects.filter(like__like=1, like__user=request.user)
    context = {'ulubione_produkty': ulubione_produkty}
    return render(request, 'favorite.html', context)

@login_required
def add_to_fav(request, id):
    if request.method == 'POST':
        product = Product.objects.get(pk=id)

        # Sprawdź, czy produkt jest już polubiony
        like = Like.objects.filter(product=product, user=request.user).first()

        if like is None:
            # Jeśli produkt nie jest polubiony, utwórz nowy obiekt Like
            like = Like.objects.create(like=1, product=product, user=request.user)
        else:
            # Jeśli produkt jest już polubiony, usuń obiekt Like
            like.delete()

    return redirect(request.META.get('HTTP_REFERER'))



class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    fields = "__all__"
    redirect_authenticated_user = False

    def get_success_url(self):
        user = self.request.user
        if not Cart.objects.filter(user=user).exists():
            Cart.objects.create(user=user)  # Tworzenie koszyka dla użytkownika przy pierwszym logowaniu
        return reverse_lazy('szart')

class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('szart')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            Cart.objects.create(user=user)  # Tworzenie koszyka dla nowego użytkownika
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('szart')
        return super(RegisterPage, self).get(*args, *kwargs)



def contact_response(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Wiadomość została wysłana.')  # Dodaj komunikat sukcesu
            return redirect('kontakt')
    else:
        form = MessageForm()

    return render(request, 'contact.html', {'form': form})


