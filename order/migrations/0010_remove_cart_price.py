# Generated by Django 4.1.7 on 2023-06-15 00:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_cart_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]
