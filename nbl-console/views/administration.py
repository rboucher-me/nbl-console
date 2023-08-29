from django.contrib import messages
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from cloud import forms
from cloud.decorators import superuser_required
from cloud.signals import config_changed


#
# Configuration
#

@method_decorator(superuser_required, name='dispatch')
class ConfigurationView(View):

    def get(self, request):
        form = forms.ConfigurationForm()

        return render(request, 'cloud/configuration.html', {
            'form': form,
        })

    def post(self, request):
        form = forms.ConfigurationForm(request.POST)

        if form.is_valid():
            form.save()

            # Transmit the config_changed signal
            config_changed.send(sender=None)

            # Populate a message warning the user that a configuration change is pending
            messages.success(request, "A new configuration change is pending. Please allow up to five minutes for it "
                                      "to take effect.")

        return render(request, 'cloud/configuration.html', {
            'form': form,
        })
