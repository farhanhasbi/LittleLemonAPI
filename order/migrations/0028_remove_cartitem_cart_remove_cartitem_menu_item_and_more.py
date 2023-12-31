# Generated by Django 4.1.7 on 2023-06-17 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0027_alter_orderitem_unique_together'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_crew',
        ),
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='menuitem',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
