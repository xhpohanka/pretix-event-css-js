import uuid

import django.db.models.deletion
import pretix_event_css_js.models
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("pretixbase", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizerAsset",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("filename", models.CharField(max_length=255, verbose_name="Filename")),
                ("content_type", models.CharField(default="application/octet-stream", max_length=255)),
                (
                    "file",
                    models.FileField(
                        max_length=500,
                        upload_to=pretix_event_css_js.models.organizer_asset_upload_to,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "organizer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event_css_js_assets",
                        to="pretixbase.organizer",
                    ),
                ),
            ],
            options={"ordering": ["filename", "created"]},
        ),
    ]
