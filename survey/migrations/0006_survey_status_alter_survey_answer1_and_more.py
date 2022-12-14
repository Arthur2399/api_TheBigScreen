# Generated by Django 4.0.2 on 2022-08-03 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0005_alter_survey_answer1_alter_survey_answer2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='survey',
            name='answer4',
            field=models.IntegerField(default=0),
        ),
    ]
