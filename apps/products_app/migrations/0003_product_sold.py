# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-26 17:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0002_product_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
    ]
