# Generated by Django 4.2.7 on 2024-04-15 03:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traininglog", "0014_remove_run_averagepace_alter_bike_averagespeed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="run",
            name="averagePace",
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="bike",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 22, 49, 741895, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="other",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 22, 49, 741895, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 22, 49, 741895, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="swim",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 22, 49, 741895, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
