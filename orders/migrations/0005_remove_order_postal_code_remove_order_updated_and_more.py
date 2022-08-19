# Generated by Django 4.0.6 on 2022-08-19 08:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0004_alter_order_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated',
        ),
        migrations.AddField(
            model_name='paystatus',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='pay_status', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.CharField(choices=[('1', 'Оплата картой на сайте'), ('2', 'Оплата картой при получении'), ('3', 'Оплата наличными при получении')], default='1', max_length=100, verbose_name='метод оплаты'),
        ),
        migrations.AlterField(
            model_name='paystatus',
            name='status',
            field=models.CharField(choices=[('1', 'Не оплаченно'), ('2', 'Оплата прошла успешно'), ('3', 'Ошибка при оплате'), ('4', 'Ожидается оплата')], default='1', max_length=100, verbose_name='Статус оплаты'),
        ),
    ]
