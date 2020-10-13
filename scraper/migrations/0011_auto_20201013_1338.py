# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-13 13:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_auto_20201012_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='picture_url',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='picture_selector',
            field=models.CharField(default='', max_length=255),
        ),
    ]
