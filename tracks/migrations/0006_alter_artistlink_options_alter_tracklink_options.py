# Generated by Django 4.0 on 2021-12-24 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("tracks", "0005_alter_artistlink_options_alter_tracklink_options_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="artistlink",
            options={"default_related_name": "link_set"},
        ),
        migrations.AlterModelOptions(
            name="tracklink",
            options={"default_related_name": "link_set"},
        ),
    ]