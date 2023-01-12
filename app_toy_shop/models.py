from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Модель категорий"""
    name = models.CharField('Категория', max_length=70, db_index=True)
    url = models.SlugField(max_length=170, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField('Название', max_length=70)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    poster = models.ImageField("Постер", upload_to="photos/", blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория',
                                 related_name="category_product")
    url = models.SlugField(max_length=170, unique=True)
    quantity = models.PositiveIntegerField('Колличество', default=1)
    is_active = models.BooleanField('Активность', default=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toy_detail', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Image(models.Model):
    """Модель изображения продукта"""
    link = models.ImageField('Изображение', upload_to='photos/', blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name="product_image")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class Star(models.Model):
    """Модель звезд"""
    star = models.PositiveSmallIntegerField('Звезда', default=1)

    def __str__(self):
        return f'{self.star}'

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звезды'
        ordering = ['-star']


class StarForProduct(models.Model):
    """Модель звезд продукта"""
    ip = models.CharField('IP', max_length=20)
    star = models.ForeignKey(Star, on_delete=models.CASCADE, verbose_name='Звезда', related_name="star_star")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name="product_star")

    def __str__(self):
        return f'{self.star} - {self.product}'

    class Meta:
        verbose_name = 'Звезда за продукт'
        verbose_name_plural = 'Звезды за продукт'


class Reviews(models.Model):
    """Модель отзывов"""
    description = models.TextField('Отзыв')
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, verbose_name='Пользователь',
                             related_name="user_reviews")
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name="product_reviews")

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.product)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-created',)


