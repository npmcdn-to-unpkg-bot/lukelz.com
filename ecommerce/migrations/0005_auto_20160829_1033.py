# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20160829_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nonmediaitem',
            name='item_fulfillment_cost',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
