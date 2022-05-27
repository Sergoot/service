# Generated by Django 4.0.4 on 2022-05-14 08:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0011_remove_exercise_is_favorite_userexercises'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userexercises',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_exercises', to=settings.AUTH_USER_MODEL),
        ),
    ]