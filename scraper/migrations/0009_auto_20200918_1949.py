# Generated by Django 3.0.8 on 2020-09-18 17:49

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
