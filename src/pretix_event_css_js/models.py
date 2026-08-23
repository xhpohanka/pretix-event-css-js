import mimetypes
import uuid

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def organizer_asset_upload_to(instance, filename):
    return "pub/{}/event-css-js-assets/{}/{}".format(
        instance.organizer.slug,
        instance.pk,
        filename,
    )


class OrganizerAsset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organizer = models.ForeignKey(
        "pretixbase.Organizer",
        on_delete=models.CASCADE,
        related_name="event_css_js_assets",
    )
    filename = models.CharField(max_length=255, verbose_name=_("Filename"))
    content_type = models.CharField(max_length=255, default="application/octet-stream")
    file = models.FileField(upload_to=organizer_asset_upload_to, max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["filename", "created"]

    @property
    def guessed_content_type(self):
        if self.content_type and self.content_type != "application/octet-stream":
            return self.content_type
        return mimetypes.guess_type(self.filename)[0] or "application/octet-stream"


@receiver(post_delete, sender=OrganizerAsset)
def organizer_asset_delete_file(sender, instance, **kwargs):
    if instance.file:
        instance.file.delete(save=False)
