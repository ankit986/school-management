# Generated by Django 3.0.5 on 2020-06-10 07:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0013_auto_20200610_0749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notice',
            name='date',
        ),
    ]
