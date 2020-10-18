# Generated by Django 2.2.16 on 2020-10-16 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201016_1441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course_prof',
            name='percent_A',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course_prof',
            name='percent_B',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course_prof',
            name='percent_C',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course_prof',
            name='percent_D',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course_prof',
            name='percent_F',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='course_prof',
            name='percent_Q',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
