# Generated by Django 3.0.8 on 2020-08-13 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20200812_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameid',
            name='stock',
            field=models.TextField(default='1'),
            preserve_default=False,
        ),
    ]
