# Generated by Django 3.0.5 on 2020-06-13 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0025_auto_20200610_0854'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='id',
        ),
        migrations.RemoveField(
            model_name='teacherextra',
            name='salary',
        ),
        migrations.AlterField(
            model_name='academics',
            name='roll',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='roll',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='studentextra',
            name='mobile',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='studentextra',
            name='roll',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='subject',
            name='subject_code',
            field=models.CharField(max_length=11, primary_key=True, serialize=False),
        ),
    ]