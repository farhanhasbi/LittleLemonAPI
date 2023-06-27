# Generated by Django 4.1.7 on 2023-06-14 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_cart_options_alter_cart_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
