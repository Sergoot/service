# Generated by Django 4.0.4 on 2022-05-10 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_exercise_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Приватное или общедоступное'),
        ),
    ]
