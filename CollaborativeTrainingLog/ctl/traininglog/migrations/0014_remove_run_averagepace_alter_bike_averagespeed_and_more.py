# Generated by Django 4.2.7 on 2024-04-15 03:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traininglog", "0013_alter_bike_elapsedtime_alter_bike_movingtime_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="run",
            name="averagePace",
        ),
        migrations.AlterField(
            model_name="bike",
            name="averageSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="bike",
            name="distance",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="bike",
            name="elapsedTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="bike",
            name="maxSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="bike",
            name="movingTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="bike",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 19, 39, 145579, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="other",
            name="averageSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="other",
            name="distance",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="other",
            name="elapsedTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="other",
            name="maxSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="other",
            name="movingTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="other",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 19, 39, 145579, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="averageCadence",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="run",
            name="distance",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="run",
            name="elapsedTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="run",
            name="maxPace",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="run",
            name="movingTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="run",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 19, 39, 145579, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="swim",
            name="averageSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="swim",
            name="distance",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="swim",
            name="elapsedTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="swim",
            name="maxSpeed",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="swim",
            name="movingTime",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="swim",
            name="startDate",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2024, 4, 15, 3, 19, 39, 145579, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
