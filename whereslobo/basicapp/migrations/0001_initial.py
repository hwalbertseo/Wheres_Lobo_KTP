# Generated by Django 5.0.3 on 2024-04-01 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Lobo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("location", models.CharField(max_length=255)),
                ("time_seen", models.DateTimeField(verbose_name="time seen")),
                ("is_claimed", models.CharField(max_length=10)),
                ("claimed_by", models.CharField(max_length=255)),
                ("claim_time", models.DateTimeField(verbose_name="time claimed")),
            ],
        ),
    ]
