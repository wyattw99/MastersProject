# Generated by Django 4.2.7 on 2024-03-25 01:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("traininglog", "0003_rename_average_speed_bike_averagespeed_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StravaAPI",
            fields=[
                ("APIid", models.AutoField(primary_key=True, serialize=False)),
                ("clientId", models.CharField(max_length=100)),
                ("clientSecret", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="StravaLogin",
            fields=[
                ("loginId", models.AutoField(primary_key=True, serialize=False)),
                ("stravaUserName", models.CharField(max_length=50)),
                ("stravaID", models.CharField(max_length=50)),
                ("stravaTokenType", models.CharField(max_length=50)),
                ("stravaExpiration", models.IntegerField()),
                ("stravaRefreshToken", models.CharField(max_length=50)),
                ("stravaAccessToken", models.CharField(max_length=50)),
                ("stravaAuthorizationCode", models.CharField(max_length=50)),
            ],
        ),
    ]