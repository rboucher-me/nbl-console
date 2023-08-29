import logging

from django.core import management
from django.dispatch import receiver, Signal


config_changed = Signal()

logger = logging.getLogger('netbox.plugins.cloud')


@receiver(config_changed)
def handle_config_change(**kwargs):
    """
    Perform necessary tasks in response to the Cloud configuration being modified.
    """
    # Run `manage.py migrate` when the configuration has been changed. This ensures
    # that any newly-enabled plugins have their migrations applied.
    management.call_command('migrate', '--no-input')
