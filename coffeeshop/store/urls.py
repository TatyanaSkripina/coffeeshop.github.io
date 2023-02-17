from django.contrib.messages import success
from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('our_story', our_story, name='our_story'),
    path('our_vision', our_vision, name='our_vision'),
    path('our_services', our_services, name='our_services'),
    path('about_us', about_us, name='about_us'),
    path('menu', menu, name='menu'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='product'),
    path('login_register/', login_register, name='login_register'),
    path('login/', user_login, name='login'),
    path('register/', register, name='register'),
    path('logout/', user_logout, name='logout'),
    path('product/<slug:slug>/save_review/', save_review, name='save_review'),
    path('contacts', contacts, name='contacts'),
    path('cart', cart, name='cart'),
    path('buy_product/<int:product_id>/<str:action>/', buy_product, name='buy_product'),
    path('to_cart/<int:product_id>/<str:action>/<str:quantity>/', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('success/', success_payment, name='success'),
    path('', MailingView.as_view(), name='mailing'),
]