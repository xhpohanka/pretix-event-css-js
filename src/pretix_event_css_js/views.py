from django.contrib.staticfiles import finders
import mimetypes

from django.contrib import messages
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic.edit import FormView
from pretix.control.permissions import OrganizerPermissionRequiredMixin
from pretix.control.views.event import EventSettingsFormView, EventSettingsViewMixin
from pretix.control.views.organizer import OrganizerDetailViewMixin, OrganizerSettingsFormView

from .forms import EventCssJsSettingsForm, OrganizerAssetUploadForm, OrganizerCssJsSettingsForm
from .models import OrganizerAsset

CACHE_MAX_AGE = 3600 * 24 * 365  # 1 year — URL changes on content update
PARKING_FONT_PATH = 'pretix_event_css_js/fonts/Parking-Regular.woff2'


def _request_organizer(request):
    return getattr(request, 'organizer', None) or request.event.organizer


class EventCssJsSettingsView(EventSettingsViewMixin, EventSettingsFormView):
    form_class = EventCssJsSettingsForm
    template_name = 'pretix_event_css_js/control_settings.html'

    def get_success_url(self):
        return reverse('plugins:pretix_event_css_js:settings', kwargs={
            'organizer': self.request.organizer.slug,
            'event': self.request.event.slug,
        })


class OrganizerCssJsSettingsView(OrganizerSettingsFormView):
    form_class = OrganizerCssJsSettingsForm
    template_name = 'pretix_event_css_js/organizer_settings.html'

    def get_success_url(self):
        return reverse('plugins:pretix_event_css_js:organizer.settings', kwargs={
            'organizer': self.request.organizer.slug,
        })


class CustomCssView(View):
    def get(self, request, *args, **kwargs):
        css = request.event.settings.get('event_css_js_css', default='')
        response = HttpResponse(css or '', content_type='text/css; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class CustomJsView(View):
    def get(self, request, *args, **kwargs):
        js = request.event.settings.get('event_css_js_js', default='')
        response = HttpResponse(js or '', content_type='application/javascript; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class OrganizerCssView(View):
    def get(self, request, *args, **kwargs):
        css = request.organizer.settings.get('organizer_css_js_css', default='')
        response = HttpResponse(css or '', content_type='text/css; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class OrganizerJsView(View):
    def get(self, request, *args, **kwargs):
        js = request.organizer.settings.get('organizer_css_js_js', default='')
        response = HttpResponse(js or '', content_type='application/javascript; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class EventOrganizerCssView(View):
    def get(self, request, *args, **kwargs):
        css = request.event.organizer.settings.get('organizer_css_js_css', default='')
        response = HttpResponse(css or '', content_type='text/css; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class EventOrganizerJsView(View):
    def get(self, request, *args, **kwargs):
        js = request.event.organizer.settings.get('organizer_css_js_js', default='')
        response = HttpResponse(js or '', content_type='application/javascript; charset=utf-8')
        if 'v' in request.GET:
            response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class ParkingFontView(View):
    def get(self, request, *args, **kwargs):
        path = finders.find(PARKING_FONT_PATH)
        if not path:
            raise Http404('Parking font asset not found')
        response = FileResponse(open(path, 'rb'), content_type='font/woff2')
        response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        return response


class OrganizerAssetUploadView(OrganizerDetailViewMixin, OrganizerPermissionRequiredMixin, FormView):
    form_class = OrganizerAssetUploadForm
    template_name = 'pretix_event_css_js/assets.html'
    permission = 'organizer.settings.general:write'

    def get_success_url(self):
        return reverse('plugins:pretix_event_css_js:assets', kwargs={
            'organizer': self.request.organizer.slug,
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assets'] = OrganizerAsset.objects.filter(organizer=self.request.organizer)
        return context

    def form_valid(self, form):
        uploaded = form.cleaned_data['file']
        asset = form.save(commit=False)
        asset.organizer = self.request.organizer
        asset.filename = uploaded.name
        asset.content_type = (
            uploaded.content_type
            or mimetypes.guess_type(uploaded.name)[0]
            or 'application/octet-stream'
        )
        asset.save()
        messages.success(self.request, _('The asset has been uploaded.'))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class OrganizerAssetDeleteView(OrganizerDetailViewMixin, OrganizerPermissionRequiredMixin, View):
    permission = 'organizer.settings.general:write'

    def post(self, request, asset, *args, **kwargs):
        try:
            obj = OrganizerAsset.objects.get(organizer=request.organizer, pk=asset)
        except OrganizerAsset.DoesNotExist:
            raise Http404(_('The requested asset does not exist.'))
        obj.delete()
        messages.success(request, _('The asset has been deleted.'))
        return HttpResponseRedirect(reverse('plugins:pretix_event_css_js:assets', kwargs={
            'organizer': request.organizer.slug,
        }))


class OrganizerAssetView(View):
    def get(self, request, asset, *args, **kwargs):
        organizer = _request_organizer(request)
        try:
            obj = OrganizerAsset.objects.get(organizer=organizer, pk=asset)
        except OrganizerAsset.DoesNotExist:
            raise Http404(_('The requested asset does not exist.'))
        obj.file.open('rb')
        response = FileResponse(obj.file, content_type=obj.guessed_content_type)
        response['Cache-Control'] = 'public, max-age={}'.format(CACHE_MAX_AGE)
        response['X-Content-Type-Options'] = 'nosniff'
        if obj.guessed_content_type in ('text/html', 'application/xhtml+xml'):
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(obj.filename.replace('"', ''))
        return response
