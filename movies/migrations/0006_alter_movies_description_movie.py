# Generated by Django 4.0.2 on 2022-05-27 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_alter_movies_duration_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='description_movie',
            field=models.TextField(max_length=500),
        ),
    ]
