from django import forms
from django.utils.translation import gettext_lazy as _
from pretix.base.forms import SettingsForm

from .models import OrganizerAsset


class EventCssJsSettingsForm(SettingsForm):
    event_css_js_css = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'class': 'monospace'}),
        label=_('Custom CSS'),
        required=False,
        help_text=_('Custom CSS rules that will be loaded on every presale page of this event.'),
    )
    event_css_js_js = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'class': 'monospace'}),
        label=_('Custom JavaScript'),
        required=False,
        help_text=_(
            'Custom JavaScript that will be loaded at the end of every presale page of this event. '
            'Use with care — incorrect code may break the shop experience for your customers.'
        ),
    )


class OrganizerCssJsSettingsForm(SettingsForm):
    organizer_css_js_css = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 18, 'class': 'monospace'}),
        label=_('Organizer CSS'),
        required=False,
        help_text=_('Custom CSS rules loaded on the public pages of all events belonging to this organizer.'),
    )
    organizer_css_js_js = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 12, 'class': 'monospace'}),
        label=_('Organizer JavaScript'),
        required=False,
        help_text=_(
            'Custom JavaScript loaded at the end of the public pages of all events belonging to this organizer. '
            'Use with care — incorrect code may break the shop experience for your customers.'
        ),
    )


class OrganizerAssetUploadForm(forms.ModelForm):
    class Meta:
        model = OrganizerAsset
        fields = ('file',)
        labels = {'file': _('Asset file')}

    def clean_file(self):
        uploaded = self.cleaned_data['file']
        if uploaded.size > 10 * 1024 * 1024:
            raise forms.ValidationError(_('The file must not be larger than 10 MB.'))
        return uploaded
