# Generated by Django 4.0.6 on 2022-08-19 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_paystatus_alter_order_paid_delete_pay_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='paid',
            field=models.CharField(choices=[(1, 'Оплата картой на сайте'), (2, 'Оплата картой при получении'), (3, 'Оплата наличными при получении')], default=1, max_length=100, verbose_name='метод оплаты'),
        ),
    ]
