# Generated by Django 4.0 on 2021-12-22 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_rename_other_url_vaccine_info_urls_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="vaccine",
            name="vaccine_type",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
