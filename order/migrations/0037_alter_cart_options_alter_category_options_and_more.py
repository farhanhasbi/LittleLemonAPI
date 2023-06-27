# Generated by Django 4.1.7 on 2023-06-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0036_alter_order_date_alter_order_total'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['pk'], 'verbose_name': 'Category'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['pk']},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'ordering': ['pk']},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.BooleanField(db_index=True),
        ),
    ]