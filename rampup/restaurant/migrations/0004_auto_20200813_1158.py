# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-08-13 11:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20200813_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resfooditem',
            name='res_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='restaurant.Restaurant'),
        ),
    ]
