# Generated by Django 3.1.7 on 2021-03-13 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_auto_20210313_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='snakefeeding',
            name='new_thing',
            field=models.IntegerField(null=True),
        ),
    ]
