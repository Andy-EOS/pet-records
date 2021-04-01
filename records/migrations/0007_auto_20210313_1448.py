# Generated by Django 3.1.7 on 2021-03-13 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0006_remove_snakefeeding_new_thing'),
    ]

    operations = [
        migrations.AddField(
            model_name='snakefeeding',
            name='type_of_food',
            field=models.CharField(choices=[('PK', 'Pinkie'), ('FZ', 'Fuzzy'), ('SM', 'Small Mouse'), ('MM', 'Medium Mouse'), ('LM', 'Large Mouse'), ('JM', 'Jumbo Mouse')], default='LM', max_length=2),
        ),
        migrations.AlterField(
            model_name='snakefeeding',
            name='animal',
            field=models.ForeignKey(limit_choices_to={'animal_type': 'SN'}, on_delete=django.db.models.deletion.CASCADE, to='records.animal'),
        ),
    ]
