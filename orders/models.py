# Create your models here.
from django.db import models

from app_toy_shop.models import Product


class Order(models.Model):
    """Модель оплаты"""
    PAYMENT_METHOD = (
        ('1', 'Оплата картой на сайте'),
        ('2', 'Оплата картой при получении'),
        ('3', 'Оплата наличными при получении')
    )
    ORDER_STATUS = (
        ('1', 'Принят'),
        ('2', 'Собран'),
        ('3', 'Передан курьеру'),
        ('4', 'Доставлен'),
        ('5', 'Аннулирован')
    )
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name="user_basket")
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.CharField('метод оплаты', max_length=100, choices=PAYMENT_METHOD, default='1')
    order_status = models.CharField('Статус Заказа', max_length=100, choices=ORDER_STATUS, default='1')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Модель деталей заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('Колличество', default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Детали заказа'
        verbose_name_plural = 'Детали заказов'


class PayStatus(models.Model):
    """Модель статуса оплаты"""
    PAYMENT_STATUS = (
        ('1', 'Не оплаченно'),
        ('2', 'Оплата прошла успешно'),
        ('3', 'Ошибка при оплате'),
        ('4', 'Ожидается оплата')
    )

    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name="pay_status", default='1')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pay')
    total_price = models.PositiveIntegerField('Сумма оплаты', default=0)
    status = models.CharField('Статус оплаты', max_length=100, choices=PAYMENT_STATUS, default='1')

    def __str__(self):
        return f'{self.order}'

    class Meta:
        verbose_name = 'Статус оплаты'
        verbose_name_plural = 'Статусы оплаты'


