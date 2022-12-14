# Generated by Django 4.0.2 on 2022-05-30 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('points', '0003_alter_credits_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_transaction', models.DateTimeField(auto_now_add=True)),
                ('total_cost', models.IntegerField()),
                ('total_credits', models.IntegerField()),
                ('balance', models.IntegerField()),
                ('credits_translation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='points.credits')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
            },
        ),
        migrations.CreateModel(
            name='TransactionDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('awards_detail', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='points.awards')),
                ('transaction_detail', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='points.transaction')),
            ],
            options={
                'verbose_name': 'TransactionDetail',
                'verbose_name_plural': 'TransactionDetails',
            },
        ),
    ]
