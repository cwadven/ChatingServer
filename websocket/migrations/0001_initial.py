# Generated by Django 3.1.6 on 2022-01-11 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GroupCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=128)),
                ('groupname', models.CharField(max_length=128)),
                ('join_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
