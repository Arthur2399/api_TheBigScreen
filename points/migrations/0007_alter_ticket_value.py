# Generated by Django 4.0.2 on 2022-05-31 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0006_ticket_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='value',
            field=models.IntegerField(default=100),
        ),
    ]
