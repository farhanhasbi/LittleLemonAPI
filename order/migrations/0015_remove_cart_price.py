# Generated by Django 4.1.7 on 2023-06-15 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0014_alter_cartitem_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='price',
        ),
    ]