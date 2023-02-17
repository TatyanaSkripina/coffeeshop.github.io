from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView

from .models import Category, Product, Size, Article, Review, OrderProduct, Order, ShippingAddress, MailingList
from django.views.generic import ListView, DetailView, CreateView
from .forms import LoginForm, RegisterForm, ReviewForm, ShippingForm, MailingForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .utils import CartForAuthenticatedUser
import stripe
from coffeeshop import settings

class MainPage(ListView):
    model = Category
    template_name = 'store/index.html'
    context_object_name = 'categories'


def our_story(request):
    article = Article.objects.all()
    context = {
        'title': f'История нашего создания',
        'article': article
    }
    return render(request, 'components/our_story.html', context)


def our_vision(request):
    article = Article.objects.all()
    context = {
        'title': f'Распространение',
        'article': article
    }
    return render(request, 'components/our_vision.html', context)


def our_services(request):
    article = Article.objects.all()
    context = {
        'title': f'Наши услуги',
        'article': article
    }
    return render(request, 'components/our_services.html', context)


def about_us(request):
    article = Article.objects.all()
    context = {
        'title': f'О нас',
        'article': article
    }
    return render(request, 'components/about_us.html', context)


def contacts(request):
    article = Article.objects.all()
    context = {
        'title': f'Контакты',
        'article': article
    }
    return render(request, 'components/contacts.html', context)


def menu(request):
    categories = Category.objects.all()
    data = []
    for category in categories:
        products = category.products.all()
        print('Products', products)
        data.append({
            'title': category,
            'products': products
        })
    context = {
        'title': f'Меню',
        'categories': data
    }
    return render(request, 'store/menu.html', context)

# class ShopProducts(ListView):
#     model = Product
#     template_name ='store/menu.html'
#     context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        product = Product.objects.get(slug=self.kwargs['slug'])
        # product.save()
        context['review_form'] = ReviewForm()
        context['reviews'] = Review.objects.filter(product=product)
        return context


def login_register(request):
    context = {
        'login_form': LoginForm(),
        'register_form': RegisterForm(),
        'title': 'Войти или зарегистрироваться'
    }
    return render(request, 'store/login_register.html', context)


def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, 'Неправильный логин или пароль')
        return redirect('login_register')


def register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Аккаунт успешно создан. Войдите в аккаунт')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())
    return redirect('login_register')


def user_logout(request):
    logout(request)
    return redirect('index')


def save_review(request, slug):
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = Product.objects.get(slug=slug)
        review.user = request.user
        review.save()
        messages.success(request, 'Ваш отзыв опубликован')
        return redirect('product', slug)


def cart(request):
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
        cart_info['title'] = 'Корзина'
        return render(request, 'store/cart.html', cart_info)
    else:
        return redirect('login_register')


def buy_product(request, product_id, action):
    if request.user.is_authenticated:
        quantity = int(request.GET.get('quantity'))
        user_cart = CartForAuthenticatedUser(request, product_id, action, quantity)
    return redirect('cart')


def to_cart(request, product_id, action, quantity):
    quantity = int(quantity)
    if request.user.is_authenticated:
        user_cart = CartForAuthenticatedUser(request, product_id, action, quantity)
    return redirect('cart')


def checkout(request):
    form = ShippingForm()
    user_cart = CartForAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    cart_info['title'] = 'Оплата'
    cart_info['form'] = form
    return render(request, 'store/checkout.html', cart_info)


def payment(request):
    form = ShippingForm(data=request.POST)
    user_cart = CartForAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    if form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.is_completed = False
        order = cart_info['order']
        address.order = order
        address.save()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']

    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Товары с Coffeeshop'
                    },
                    'unit_amount': int(total_price * 100)
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success')),
        cancel_url=request.build_absolute_uri(reverse('checkout')),
    )
    return redirect(session.url, 303)

def success_payment(request):
    user_cart = CartForAuthenticatedUser(request)
    user_cart.clear()
    return render(request, 'store/success.html')


class MailingView(CreateView):
    model = MailingList
    form_class = MailingForm
    template_name = 'store/index.html'
