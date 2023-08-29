import os

from django import forms
from django.conf import settings

from utilities.forms import ChoiceField
from .choices import *
from .utils import save_config

CONFIG = settings.PLUGINS_CONFIG['cloud']

REQUIRED_AUTH_FIELDS = {
    AUTH_BACKEND_AZUREAD: (
        'SOCIAL_AUTH_AZUREAD_OAUTH2_KEY',
        'SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET',
    ),
    AUTH_BACKEND_OKTA_OIDC: (
        'SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY',
        'SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET',
        'SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL',
    ),
}


class BootstrapMixin:
    """
    Add the base Bootstrap CSS classes to form elements.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exempt_widgets = [
            forms.CheckboxInput,
            forms.CheckboxSelectMultiple,
            forms.FileInput,
            forms.RadioSelect,
            forms.Select,
        ]

        for field_name, field in self.fields.items():

            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()

            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'

            if field.widget.__class__ == forms.CheckboxInput:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join((css, 'form-check-input')).strip()

            if field.widget.__class__ == forms.Select:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join((css, 'form-select')).strip()


class ConfirmationForm(BootstrapMixin, forms.Form):
    """
    Used to confirm user intent before dangerous operations (e.g. object deletion)
    """
    confirm = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput()
    )


class FileUploadForm(BootstrapMixin, forms.Form):
    file = forms.FileField()
    overwrite = forms.BooleanField(
        required=False
    )


class FileDeleteForm(ConfirmationForm):
    files = forms.MultipleChoiceField(
        choices=[],
        widget=forms.MultipleHiddenInput()
    )

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Use directory listing as field choices
        self.fields['files'].choices = [
            (name, name) for name in os.listdir(path)
        ]


#
# Configuration
#

class ConfigurationForm(BootstrapMixin, forms.Form):
    # Login & authentication
    LOGIN_PERSISTENCE = forms.BooleanField(
        required=False,
        help_text="Refresh user session on every request"
    )
    LOGIN_TIMEOUT = forms.IntegerField(
        required=False,
        help_text="User login duration (in seconds)"
    )
    REMOTE_AUTH_BACKEND = ChoiceField(
        choices=AUTH_BACKEND_CHOICES,
        required=False,
        label='Authentication backend',
        help_text='Select a backend to enable remote authentication, and complete the relevant configuration below.'
    )
    # Azure AD
    SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = forms.CharField(
        required=False,
        label='Application (client) ID'
    )
    SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = forms.CharField(
        required=False,
        label='Secret'
    )
    # Okta OIDC
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = forms.CharField(
        required=False,
        label='Client ID'
    )
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = forms.CharField(
        required=False,
        label='Client secret'
    )
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL = forms.CharField(
        required=False,
        label='API URL',
        help_text="This will typically be in the form `https://{OKTA-DOMAIN}/oauth2/`"
    )

    # Date & time formatting
    DATE_FORMAT = ChoiceField(
        choices=DATE_FORMAT_CHOICES,
        required=False
    )
    SHORT_DATE_FORMAT = ChoiceField(
        choices=SHORT_DATE_FORMAT_CHOICES,
        required=False
    )
    TIME_FORMAT = ChoiceField(
        choices=TIME_FORMAT_CHOICES,
        required=False
    )
    SHORT_TIME_FORMAT = ChoiceField(
        choices=SHORT_TIME_FORMAT_CHOICES,
        required=False
    )

    # Plugins
    PLUGINS = forms.MultipleChoiceField(
        choices=PLUGIN_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Plugins enabled'
    )
    PLUGINS_CONFIG = forms.JSONField(
        required=False,
        help_text="Enter plugin configuration as a JSON object, with each root-level key mapping to a "
                  "plugin name. For example:<br /><code>{\"plugin_name\": {\"parameter_name\": 123}}</code>",
        label='Plugin configuration',
        widget=forms.Textarea(attrs={'style': 'font-family: monospace'})
    )

    def clean(self):

        # Validate remote auth backend configuration parameters (if enabled)
        for field in REQUIRED_AUTH_FIELDS.get(self.cleaned_data.get('REMOTE_AUTH_BACKEND'), []):
            if not self.cleaned_data[field]:
                self.add_error(field, 'This field is required.')

    def save(self):
        """
        Call save_config() to send the updated configuration parameters to the platform.
        """
        # Strip any empty values
        self.cleaned_data = {
            field: value for field, value in self.cleaned_data.items() if value not in (None, '')
        }

        save_config(self.cleaned_data)

    def get_initial_for_field(self, field, field_name):
        """
        Populate initial data for config parameter fields using the active Django settings.
        """
        if hasattr(settings, field_name):
            return getattr(settings, field_name)
        return super().get_initial_for_field(field, field_name)


#
# Services
#

class ServiceRestartForm(BootstrapMixin, forms.Form):
    confirm = forms.BooleanField()
