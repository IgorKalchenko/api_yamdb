# Generated by Django 2.2.16 on 2022-03-21 09:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0006_auto_20220321_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(error_messages={'invalid_date': 'Значение даты введено неправильно'}, validators=[django.core.validators.MaxValueValidator(2022), django.core.validators.MinValueValidator(0)], verbose_name='Год выпуска'),
        ),
    ]