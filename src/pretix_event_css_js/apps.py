from django.utils.translation import gettext_lazy

from pretix.base.plugins import PLUGIN_LEVEL_ORGANIZER

from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 2.7 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_event_css_js"
    verbose_name = gettext_lazy("Organizer CSS & JS")

    class PretixPluginMeta:
        name = gettext_lazy("Organizer CSS & JS")
        author = "Nico Knoll"
        description = gettext_lazy(
            "Inject custom CSS and JavaScript into all presale pages of an organizer, with optional event overrides."
        )
        visible = True
        version = __version__
        category = "CUSTOMIZATION"
        compatibility = "pretix>=2026.6.0"
        level = PLUGIN_LEVEL_ORGANIZER
        settings_links = [
            (gettext_lazy("Organizer CSS & JS"), "plugins:pretix_event_css_js:organizer.settings", {}),
        ]

    def ready(self):
        from . import signals  # NOQA

    def uninstalled(self, organizer):
        from .models import OrganizerAsset

        organizer.settings.delete('organizer_css_js_css')
        organizer.settings.delete('organizer_css_js_js')
        OrganizerAsset.objects.filter(organizer=organizer).delete()
