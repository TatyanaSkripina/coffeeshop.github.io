from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Product, Size, Article
from django.views.generic import ListView, DetailView

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
    #products = Product.objects.all()
    context = {
        'title': f'Меню',
        'categories': data
    }
    return render(request, 'store/menu.html', context)


# class ShopProducts(ListView):
#     model = Product
#     template_name ='store/menu.html'
#     context_object_name = 'products'