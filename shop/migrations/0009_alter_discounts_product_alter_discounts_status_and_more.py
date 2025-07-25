# Generated by Django 5.1.1 on 2025-05-14 16:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_products_discount_alter_products_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discounts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='shop.products'),
        ),
        migrations.AlterField(
            model_name='discounts',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='products',
            name='discount',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.discounts'),
        ),
    ]
