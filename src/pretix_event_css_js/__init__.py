__version__ = "2.0.0"

try:
    from pretix_event_css_js.apps import PluginApp
    PretixPluginMeta = PluginApp.PretixPluginMeta
except ImportError:
    pass
