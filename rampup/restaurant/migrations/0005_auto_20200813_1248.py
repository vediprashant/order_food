# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2020-08-13 12:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_auto_20200813_1158'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ordered_Item',
            new_name='OrderedItem',
        ),
    ]