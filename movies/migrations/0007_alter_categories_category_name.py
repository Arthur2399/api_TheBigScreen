# Generated by Django 4.0.2 on 2022-05-27 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_alter_movies_description_movie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category_name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
