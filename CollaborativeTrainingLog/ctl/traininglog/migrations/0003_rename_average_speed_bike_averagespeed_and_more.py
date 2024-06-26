# Generated by Django 4.2.7 on 2024-03-25 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        (
            "traininglog",
            "0002_alter_athlete_user_alter_coach_user_swim_run_other_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="bike",
            old_name="average_speed",
            new_name="averageSpeed",
        ),
        migrations.RenameField(
            model_name="bike",
            old_name="max_speed",
            new_name="maxSpeed",
        ),
        migrations.RenameField(
            model_name="other",
            old_name="average_speed",
            new_name="averageSpeed",
        ),
        migrations.RenameField(
            model_name="other",
            old_name="max_speed",
            new_name="maxSpeed",
        ),
        migrations.RenameField(
            model_name="run",
            old_name="average_cadence",
            new_name="averageCadence",
        ),
        migrations.RenameField(
            model_name="run",
            old_name="average_speed",
            new_name="averagePace",
        ),
        migrations.RenameField(
            model_name="run",
            old_name="max_speed",
            new_name="maxPace",
        ),
        migrations.RenameField(
            model_name="swim",
            old_name="average_speed",
            new_name="averageSpeed",
        ),
        migrations.RenameField(
            model_name="swim",
            old_name="max_speed",
            new_name="maxSpeed",
        ),
    ]
