# Generated by Django 4.1.7 on 2023-06-16 11:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='unit_price',
        ),
    ]