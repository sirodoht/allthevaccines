# Generated by Django 4.2.7 on 2023-11-30 11:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0012_disease_notes"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Subscription",
        ),
    ]
