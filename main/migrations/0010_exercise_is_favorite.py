# Generated by Django 4.0.4 on 2022-05-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_exercise_user_exercise_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='is_favorite',
            field=models.BooleanField(default=False, verbose_name='Избранное'),
        ),
    ]
