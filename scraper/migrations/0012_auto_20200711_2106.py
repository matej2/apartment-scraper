# Generated by Django 3.0.8 on 2020-07-11 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0011_auto_20200711_2012'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apartmentparameter',
            old_name='parameters',
            new_name='parameter',
        ),
    ]
