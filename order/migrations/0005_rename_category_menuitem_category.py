# Generated by Django 4.1.7 on 2023-06-13 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_cart_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menuitem',
            old_name='Category',
            new_name='category',
        ),
    ]
