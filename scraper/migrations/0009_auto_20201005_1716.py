# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-05 17:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_auto_20200716_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='description_selector',
            field=models.CharField(default='', max_length=255),
        ),
    ]