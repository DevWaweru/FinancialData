# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-04 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finviz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='market',
            name='change',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='market',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='market',
            name='volume',
            field=models.IntegerField(),
        ),
    ]
