# Generated by Django 4.0 on 2021-12-20 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0008_vaccine_vaccine_class"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vaccine",
            old_name="other_url",
            new_name="info_urls",
        ),
        migrations.RemoveField(
            model_name="vaccine",
            name="wikipedia_url",
        ),
    ]
