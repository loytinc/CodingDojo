# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-28 00:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0009_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quantities', to='products_app.Product'),
        ),
    ]