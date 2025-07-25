# Generated by Django 5.1.5 on 2025-05-19 15:30

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_alter_discounts_product_alter_discounts_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.CharField(choices=[('framed', 'Замовлення оформлено'), ('transit', 'Доставляється'), ('delivered', 'Доставлено'), ('canceled', 'Скасовано')], default='framed', max_length=20),
        ),
        migrations.AlterField(
            model_name='reviews',
            name='rating',
            field=models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
