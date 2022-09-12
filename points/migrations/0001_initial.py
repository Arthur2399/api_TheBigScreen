# Generated by Django 4.0.2 on 2022-05-30 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Awards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_award', models.CharField(max_length=255)),
                ('number_award', models.IntegerField()),
                ('photo_award', models.ImageField(max_length=255, upload_to='awards/')),
            ],
            options={
                'verbose_name': 'Award',
                'verbose_name_plural': 'Awards',
            },
        ),
    ]
