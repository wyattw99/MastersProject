# Generated by Django 4.2.7 on 2024-03-25 00:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("traininglog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="athlete",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="athleteProfile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="coach",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="coachProfile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="Swim",
            fields=[
                ("activityId", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("movingTime", models.DurationField()),
                ("elapsedTime", models.DurationField()),
                ("stravaId", models.CharField(max_length=30)),
                ("startDate", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("hasHeartrate", models.BooleanField(default=False)),
                ("averageHeartrate", models.IntegerField(blank=True, null=True)),
                ("maxHeartrate", models.IntegerField(blank=True, null=True)),
                ("stravaManual", models.BooleanField(default=False)),
                ("manual", models.BooleanField(default=False)),
                ("hasGps", models.BooleanField(default=True)),
                ("average_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                ("max_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "athlete",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="swims",
                        to="traininglog.athlete",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                ("activityId", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("movingTime", models.DurationField()),
                ("elapsedTime", models.DurationField()),
                ("stravaId", models.CharField(max_length=30)),
                ("startDate", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("hasHeartrate", models.BooleanField(default=False)),
                ("averageHeartrate", models.IntegerField(blank=True, null=True)),
                ("maxHeartrate", models.IntegerField(blank=True, null=True)),
                ("stravaManual", models.BooleanField(default=False)),
                ("manual", models.BooleanField(default=False)),
                ("hasGps", models.BooleanField(default=True)),
                ("average_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                ("max_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "average_cadence",
                    models.DecimalField(decimal_places=2, max_digits=3),
                ),
                (
                    "athlete",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="runs",
                        to="traininglog.athlete",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Other",
            fields=[
                ("activityId", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("movingTime", models.DurationField()),
                ("elapsedTime", models.DurationField()),
                ("stravaId", models.CharField(max_length=30)),
                ("startDate", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("hasHeartrate", models.BooleanField(default=False)),
                ("averageHeartrate", models.IntegerField(blank=True, null=True)),
                ("maxHeartrate", models.IntegerField(blank=True, null=True)),
                ("stravaManual", models.BooleanField(default=False)),
                ("manual", models.BooleanField(default=False)),
                ("hasGps", models.BooleanField(default=True)),
                ("average_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                ("max_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                ("activityType", models.CharField(max_length=50)),
                (
                    "athlete",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="otherActivites",
                        to="traininglog.athlete",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Bike",
            fields=[
                ("activityId", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=50)),
                ("movingTime", models.DurationField()),
                ("elapsedTime", models.DurationField()),
                ("stravaId", models.CharField(max_length=30)),
                ("startDate", models.DateTimeField()),
                ("distance", models.DecimalField(decimal_places=2, max_digits=10)),
                ("hasHeartrate", models.BooleanField(default=False)),
                ("averageHeartrate", models.IntegerField(blank=True, null=True)),
                ("maxHeartrate", models.IntegerField(blank=True, null=True)),
                ("stravaManual", models.BooleanField(default=False)),
                ("manual", models.BooleanField(default=False)),
                ("hasGps", models.BooleanField(default=True)),
                ("average_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                ("max_speed", models.DecimalField(decimal_places=2, max_digits=5)),
                (
                    "athlete",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bikes",
                        to="traininglog.athlete",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
