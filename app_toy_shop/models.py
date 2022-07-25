from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.db import models

from app_toy_shop.validators import phone_validator


class Category(models.Model):
    name = models.CharField('Категория', max_length=70)
    url = models.SlugField(max_length=170, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField('Название', max_length=70)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория',
                                 related_name="category_product")
    url = models.SlugField(max_length=170, unique=True)
    is_active = models.BooleanField('Активность', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Image(models.Model):
    link = models.ImageField('Изображение', upload_to='photos/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name="product_image")

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class User(AbstractUser):
    phone = models.CharField('телефон', validators=[phone_validator], max_length=13)

    def __str__(self):
        return self.username




class Basket(models.Model):
    total_price = models.DecimalField('Окончательная цена', max_digits=5, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name="user_basket")
    is_active = models.BooleanField('Активность', default=True)

    def __str__(self):
        return f'{self.total_price} {self.user}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name="product_item")
    count = models.PositiveSmallIntegerField('Колличество', default=1)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='Корзина', related_name="basket_item")

    def __str__(self):
        return f'{self.product} {self.count}'

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name="user_address")
    town = models.CharField('Город', max_length=30)
    street = models.CharField('Улица', max_length=30, null=True)
    house = models.CharField('Дом', max_length=30)
    flat = models.CharField('Квартира', max_length=30, null=True)

    def __str_(self):
        return f'{self.user} - {self.street}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class Pay(models.Model):
    METHOD_PAY_CHOICES = [
        ('cash_delivery', 'Наличные курьеру'),
        ('card', 'Картой на сайте'),
        ('card_delivery', 'Картой курьеру'),
    ]
    method_pay = models.CharField('Способ оплаты', max_length=50, choices=METHOD_PAY_CHOICES, default='card')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, verbose_name='Адрес', related_name="address_pay")

    def __str_(self):
        return f'{self.method_pay} - {self.address}'

    class Meta:
        verbose_name = 'Оплата'


class Order(models.Model):
    STATUS = [
        ('payment made', 'Оплаченно'),
        ('on the assembly', 'На сборке'),
        ('delivered', 'Доставленно'),
    ]
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, verbose_name='Корзина', related_name="basket_order")
    date = models.DateTimeField('Дата', auto_now=True)
    method_pay = models.ForeignKey(Pay, on_delete=models.CASCADE, verbose_name='Метод оплаты', related_name="pay_order")
    status = models.CharField('Статус', max_length=50, choices=STATUS, default='payment made')

    def __str__(self):
        return f'{self.basket}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Star(models.Model):
    star = models.PositiveSmallIntegerField('Звезда', default=1)

    def __str__(self):
        return self.star

    class Meta:
        verbose_name = 'Звезда'
        verbose_name_plural = 'Звезды'


class StarForProduct(models.Model):
    ip = models.CharField('IP', max_length=20)
    star = models.ForeignKey(Star, on_delete=models.CASCADE, verbose_name='Звезда', related_name="star_star")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name="product_star")

    def __str__(self):
        return f'{self.star} - {self.product}'

    class Meta:
        verbose_name = 'Звезда за продукт'
        verbose_name_plural = 'Звезды за продукт'


class Reviews(models.Model):
    description = models.TextField('Отзыв')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь',
                             related_name="user_reviews")
    created = models.DateTimeField('Дата создания', auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт',
                                related_name="product_reviews")

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, self.product)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('created',)


class Room(models.Model):
    number = models.PositiveIntegerField('Номер комнаты')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Администратор',
                              related_name="user_admin_room")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь',
                                related_name="user_room")

    def __str__(self):
        return f'{self.number} - {self.user}'

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Комната', related_name="number_room")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь',
                             related_name="user_message")
    text = models.TextField('Текст сообщения')
    date = models.DateTimeField('Дата', auto_now=True)
    is_active = models.BooleanField('Статус', default=True)

    def __str__(self):
        return f'{self.user} - {self.text}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
