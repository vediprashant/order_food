# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-08-14 08:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20200814_0617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordereditem',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='restaurant.Order'),
        ),
    ]
