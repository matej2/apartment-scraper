# Generated by Django 3.0.8 on 2020-07-11 18:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0010_apartmentparameters'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApartmentParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=500, null=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Apartment')),
            ],
        ),
        migrations.RemoveField(
            model_name='parameter',
            name='value',
        ),
        migrations.DeleteModel(
            name='ApartmentParameters',
        ),
        migrations.AddField(
            model_name='apartmentparameter',
            name='parameters',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraper.Parameter'),
        ),
    ]
