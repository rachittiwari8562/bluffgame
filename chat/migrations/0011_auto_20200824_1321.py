# Generated by Django 3.0.8 on 2020-08-24 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0010_auto_20200824_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameid',
            name='chance',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gameid',
            name='decks',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
