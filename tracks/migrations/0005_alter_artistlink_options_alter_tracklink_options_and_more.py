# Generated by Django 4.0 on 2021-12-24 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tracks", "0004_alter_artistlink_artist_alter_tracklink_track"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="artistlink",
            options={"default_related_name": "link"},
        ),
        migrations.AlterModelOptions(
            name="tracklink",
            options={"default_related_name": "link"},
        ),
        migrations.AlterField(
            model_name="artistlink",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tracks.artist"
            ),
        ),
        migrations.AlterField(
            model_name="tracklink",
            name="track",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="tracks.track"
            ),
        ),
    ]
