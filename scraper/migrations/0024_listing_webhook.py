# Generated by Django 3.2.8 on 2021-10-28 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_delete_webhooklisting'),
        ('scraper', '0023_auto_20211028_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='webhook',
            field=models.ManyToManyField(blank=True, null=True, to='config.Webhook'),
        ),
    ]
