from django.db import models

# Create your models here.
from django.db import models
from app_toy_shop.models import Product
from user.models import User
class Order(models.Model):
    PAYMENT_METHOD = [
        (1, 'Оплата картой на сайте'),
        (2, 'Оплата картой при получении'),
        (3, 'Оплата наличными при получении')
    ]
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='Пользователь', related_name="user_basket")
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.CharField('метод оплаты', max_length=10, choices=PAYMENT_METHOD, default=1)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity



class PayStatus(models.Model):


    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pay')
    status = models.BooleanField('Статус', default=False)

    def __str__(self):
        return f'{self.order}'




