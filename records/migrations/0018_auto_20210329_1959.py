# Generated by Django 3.1.7 on 2021-03-29 18:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0017_gecko_feedings_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gecko',
            name='feedings_started',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
