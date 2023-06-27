# Generated by Django 4.1.7 on 2023-06-22 14:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order', '0037_alter_cart_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_crew',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
