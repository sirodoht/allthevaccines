# Generated by Django 4.0 on 2022-01-04 23:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0011_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="disease",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
