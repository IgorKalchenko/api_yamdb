# Generated by Django 3.2.3 on 2022-03-20 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220320_1531'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.title', verbose_name='Произведение'),
        ),
    ]