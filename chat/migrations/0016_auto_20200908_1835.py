# Generated by Django 3.0.8 on 2020-09-08 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_auto_20200908_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameid',
            name='typ',
            field=models.IntegerField(default=-1),
        ),
    ]
