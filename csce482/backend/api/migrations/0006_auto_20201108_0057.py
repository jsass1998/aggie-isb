# Generated by Django 2.2.16 on 2020-11-08 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201107_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='term',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='avg_day_length',
            field=models.TimeField(default='05:00:00'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='avg_endtime',
            field=models.TimeField(default='15:00:00'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='avg_starttime',
            field=models.TimeField(default='12:00:00'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='description',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='free_on_friday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='free_on_monday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='free_on_thursday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='free_on_tuesday',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='free_on_wednesday',
            field=models.BooleanField(default=False),
        ),
    ]
