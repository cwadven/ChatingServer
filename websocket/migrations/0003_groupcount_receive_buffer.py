# Generated by Django 3.1.6 on 2022-01-13 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('websocket', '0002_groupchatlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupcount',
            name='receive_buffer',
            field=models.CharField(max_length=128),
        ),
    ]
