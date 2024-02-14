# Generated by Django 4.2.2 on 2023-07-10 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szartapp', '0012_product_sold_alter_product_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='like',
            field=models.PositiveSmallIntegerField(choices=[(0, 'niepolubione'), (1, 'polubione')], default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='sold',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Zapytaj o podobne'), (0, 'Kup')], default=0),
        ),
    ]
