
import hashlib

from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from pretix.control.signals import nav_event_settings, nav_organizer
from pretix.multidomain.urlreverse import eventreverse
from pretix.presale.signals import global_html_footer, global_html_head, html_footer, html_head


def _content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]


@receiver(nav_event_settings, dispatch_uid='event_css_js_nav_settings')
def navbar_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    return [{
        'label': _('Event CSS & JS'),
        'url': reverse('plugins:pretix_event_css_js:settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_event_css_js' and url.url_name == 'settings',
    }]


@receiver(nav_organizer, dispatch_uid='event_css_js_nav_organizer_settings')
def navbar_organizer_settings(sender, request=None, organizer=None, **kwargs):
    organizer = organizer or getattr(request, 'organizer', None)
    if organizer is None or request is None:
        return []
    if not request.user.has_organizer_permission(organizer, 'organizer.settings.general:write', request=request):
        return []
    url = resolve(request.path_info)
    settings_url = reverse('plugins:pretix_event_css_js:organizer.settings', kwargs={
            'organizer': organizer.slug,
        })
    assets_url = reverse('plugins:pretix_event_css_js:assets', kwargs={
        'organizer': organizer.slug,
    })
    return [{
        'label': _('Organizer CSS & JS'),
        'url': settings_url,
        'active': url.namespace == 'plugins:pretix_event_css_js',
        'icon': 'paint-brush',
        'children': [
            {
                'label': _('Code'),
                'url': settings_url,
                'active': url.url_name == 'organizer.settings',
            },
            {
                'label': _('Assets'),
                'url': assets_url,
                'active': url.url_name in ('assets', 'asset.delete'),
            },
        ],
    }]


def _link(url):
    return format_html('<link rel="stylesheet" type="text/css" href="{}">', url)


def _script(url):
    return format_html('<script src="{}"></script>', url)


def _versioned(url, content):
    return '{}?v={}'.format(url, _content_hash(content))


@receiver(html_head, dispatch_uid="pretix_event_css_js_html_head")
def r_html_head(sender, request=None, **kwargs):
    css = sender.settings.get('event_css_js_css', default='')
    links = []
    if css and css.strip():
        links.append(_link(_versioned(eventreverse(sender, 'plugins:pretix_event_css_js:custom.css'), css)))
    return ''.join(links)


@receiver(html_footer, dispatch_uid="pretix_event_css_js_html_footer")
def html_foot_presale(sender, request=None, **kwargs):
    js = sender.settings.get('event_css_js_js', default='')
    scripts = []
    if js and js.strip():
        scripts.append(_script(_versioned(eventreverse(sender, 'plugins:pretix_event_css_js:custom.js'), js)))
    return ''.join(scripts)


@receiver(global_html_head, dispatch_uid='event_css_js_global_html_head')
def global_html_head_presale(sender, request=None, **kwargs):
    if request is None:
        return ''
    event = getattr(request, 'event', None)
    organizer = event.organizer if event is not None else getattr(request, 'organizer', None)
    if organizer is None or 'pretix_event_css_js' not in organizer.get_plugins():
        return ''
    css = organizer.settings.get('organizer_css_js_css', default='')
    if not css or not css.strip():
        return ''
    url = eventreverse(event or organizer, 'plugins:pretix_event_css_js:organizer.css')
    return _link(_versioned(url, css))


@receiver(global_html_footer, dispatch_uid='event_css_js_global_html_footer')
def global_html_footer_presale(sender, request=None, **kwargs):
    if request is None:
        return ''
    event = getattr(request, 'event', None)
    organizer = event.organizer if event is not None else getattr(request, 'organizer', None)
    if organizer is None or 'pretix_event_css_js' not in organizer.get_plugins():
        return ''
    js = organizer.settings.get('organizer_css_js_js', default='')
    if not js or not js.strip():
        return ''
    url = eventreverse(event or organizer, 'plugins:pretix_event_css_js:organizer.js')
    return _script(_versioned(url, js))
