# Generated by Django 5.1.2 on 2024-11-19 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapka', '0004_userinfo_clickcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='wiek',
            field=models.IntegerField(default=0),
        ),
    ]
