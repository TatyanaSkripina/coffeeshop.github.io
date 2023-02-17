from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPage.as_view(), name='index'),
    path('our_story', our_story, name='our_story'),
    path('our_vision', our_vision, name='our_vision'),
    path('our_services', our_services, name='our_services'),
    path('about_us', about_us, name='about_us'),
    path('menu', menu, name='menu'),
]