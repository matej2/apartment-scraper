# Generated by Django 3.0.5 on 2020-06-05 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20200605_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='rent',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
