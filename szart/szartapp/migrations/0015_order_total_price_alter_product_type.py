# Generated by Django 4.2.2 on 2023-07-11 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('szartapp', '0014_alter_like_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Ceramika'), (0, 'Malarstwo')], default=0),
        ),
    ]
