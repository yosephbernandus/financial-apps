# Generated by Django 3.2.6 on 2021-08-28 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('financial_goals', '0002_auto_20210606_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialgoal',
            name='amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='goalsavingstransaction',
            name='amount',
            field=models.FloatField(default=0),
        ),
    ]