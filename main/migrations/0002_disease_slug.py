# Generated by Django 4.0 on 2021-12-20 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="disease",
            name="slug",
            field=models.CharField(default="disease-slug-example", max_length=100),
            preserve_default=False,
        ),
    ]
