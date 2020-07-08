# Generated by Django 3.0.8 on 2020-07-08 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_auto_20200612_2242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('limit', models.IntegerField(null=True)),
                ('title_selector', models.CharField(max_length=255)),
                ('rent_selector', models.CharField(max_length=255)),
                ('contact_selector', models.CharField(max_length=255)),
            ],
        ),
    ]
