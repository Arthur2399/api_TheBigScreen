# Generated by Django 4.0.2 on 2022-05-30 18:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('points', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='credits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_credits', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='user_credits', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
                'verbose_name': 'Credit',
                'verbose_name_plural': 'Credits',
            },
        ),
    ]
