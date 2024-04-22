# Generated by Django 4.2.7 on 2024-04-14 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traininglog", "0006_workout_assigneddate_workout_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="workout",
            name="athlete",
        ),
        migrations.AddField(
            model_name="workout",
            name="athletes",
            field=models.ManyToManyField(
                related_name="assignedWorkouts", to="traininglog.athlete"
            ),
        ),
        migrations.AlterField(
            model_name="bike",
            name="hasGps",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="bike",
            name="manual",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="other",
            name="hasGps",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="other",
            name="manual",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="run",
            name="hasGps",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="run",
            name="manual",
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name="swim",
            name="hasGps",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="swim",
            name="manual",
            field=models.BooleanField(default=True),
        ),
    ]
