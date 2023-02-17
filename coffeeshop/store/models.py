from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название категории')
    image = models.ImageField(upload_to='categories', blank=True, null=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Size(models.Model):
    title = models.CharField(max_length=100, verbose_name='Размер порции')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер порции')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    quantity = models.IntegerField(default=0, verbose_name="Кол-во")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название статьи')
    content = models.TextField(verbose_name='Описание статьи')
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', default=None)
    text = models.TextField(verbose_name='Отзыв')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = sum([product.quantity for product in order_products])
        return total_quantity

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name='Количество')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата оформления заказа')

    @property
    def get_total_price(self):
        total_price = self.product.price * self.quantity
        return total_price

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'


class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    city = models.CharField(max_length=255, verbose_name='Город')
    zipcode = models.CharField(max_length=255, verbose_name='Почтовый индекс')
    phone = models.CharField(default='+998', max_length=255, verbose_name='Телефон')
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарий к заказу')
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class MailingList(models.Model):
    name = models.TextField(max_length=255, verbose_name='Имя')
    email = models.EmailField(max_length=255, verbose_name='Почта')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return self.email
