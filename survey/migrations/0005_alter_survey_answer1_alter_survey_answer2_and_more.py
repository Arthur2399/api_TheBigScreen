# Generated by Django 4.0.2 on 2022-07-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0004_alter_survey_answer1_alter_survey_answer2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='answer1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer4',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
