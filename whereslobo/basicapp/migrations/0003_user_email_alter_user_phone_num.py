# Generated by Django 5.0.3 on 2024-04-01 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("basicapp", "0002_user_alter_lobo_claim_time_alter_lobo_time_seen"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="email",
            field=models.CharField(default="Default", max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_Num",
            field=models.IntegerField(default=0),
        ),
    ]