# Generated by Django 4.1.7 on 2023-06-20 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0034_alter_menuitem_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ['pk'], 'verbose_name': 'Menu item'},
        ),
    ]
