# Generated by Django 4.0 on 2021-12-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_disease_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="disease",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="disease",
            name="slug",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
