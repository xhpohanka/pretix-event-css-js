from django.urls import path, re_path
from pretix.multidomain import event_url

from .views import (
    CustomCssView, CustomJsView, EventCssJsSettingsView, EventOrganizerCssView,
    EventOrganizerJsView, OrganizerCssJsSettingsView, OrganizerCssView, OrganizerJsView,
    OrganizerAssetDeleteView, OrganizerAssetUploadView, OrganizerAssetView, ParkingFontView,
)

event_patterns = [
    event_url(r'^event_css_js/assets/(?P<asset>[0-9a-f-]+)/$', OrganizerAssetView.as_view(), name='asset'),
    event_url(r'^event_css_js/parking\.woff2$', ParkingFontView.as_view(), name='parking.woff2'),
    event_url(r'^event_css_js/organizer\.css$', EventOrganizerCssView.as_view(), name='organizer.css'),
    event_url(r'^event_css_js/organizer\.js$', EventOrganizerJsView.as_view(), name='organizer.js'),
    event_url(r'^event_css_js/custom\.css$', CustomCssView.as_view(), name='custom.css'),
    event_url(r'^event_css_js/custom\.js$', CustomJsView.as_view(), name='custom.js'),
]

organizer_patterns = [
    path('event_css_js/assets/<uuid:asset>/', OrganizerAssetView.as_view(), name='asset'),
    path('event_css_js/parking.woff2', ParkingFontView.as_view(), name='parking.woff2'),
    path('event_css_js/organizer.css', OrganizerCssView.as_view(), name='organizer.css'),
    path('event_css_js/organizer.js', OrganizerJsView.as_view(), name='organizer.js'),
]

urlpatterns = [
    re_path(
        r'^control/organizer/(?P<organizer>[^/]+)/event_css_js/assets$',
        OrganizerAssetUploadView.as_view(),
        name='assets',
    ),
    re_path(
        r'^control/organizer/(?P<organizer>[^/]+)/event_css_js/assets/(?P<asset>[0-9a-f-]+)/delete$',
        OrganizerAssetDeleteView.as_view(),
        name='asset.delete',
    ),
    re_path(
        r'^control/organizer/(?P<organizer>[^/]+)/event_css_js/settings$',
        OrganizerCssJsSettingsView.as_view(),
        name='organizer.settings',
    ),
    re_path(
        r'^control/event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/event_css_js/settings$',
        EventCssJsSettingsView.as_view(),
        name='settings',
    ),
]
