# Generated by Django 2.2.16 on 2022-03-21 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('', 'Аноним'), ('admin', 'administator'), ('user', 'user_auth'), ('moderator', 'moderator')], default='user', max_length=50, verbose_name='Роль'),
        ),
    ]