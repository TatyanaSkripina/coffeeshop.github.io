from django.db import models

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