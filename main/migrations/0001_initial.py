# Generated by Django 4.0 on 2021-12-20 02:26

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Vaccine",
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
                ("trade_name", models.CharField(max_length=100)),
                ("manufacturer", models.CharField(max_length=100)),
            ],
            options={
                "ordering": ["trade_name"],
            },
        ),
        migrations.CreateModel(
            name="Disease",
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
                ("name", models.CharField(max_length=100)),
                ("wikipedia_url", models.CharField(max_length=100)),
                ("vaccines", models.ManyToManyField(to="main.Vaccine")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
