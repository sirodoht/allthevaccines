# Generated by Django 4.0 on 2021-12-20 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_vaccine_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vaccine",
            name="slug",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="vaccine",
            name="trade_name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
