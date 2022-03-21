# Generated by Django 2.2.16 on 2022-03-21 09:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_review_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(error_messages={'invalid_date': 'Значение даты введено неправильно'}, max_length=4, validators=[django.core.validators.MaxValueValidator(2022)], verbose_name='Год выпуска'),
        ),
    ]