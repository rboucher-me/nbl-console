import datetime
import os

from django.conf import settings
from django.utils.decorators import method_decorator
from extras.scripts import get_scripts

from cloud.decorators import superuser_required
from .generic import FileDeleteView, FileManagementView

__all__ = (
    'ScriptDeleteView',
    'ScriptManagementView',
)


@method_decorator(superuser_required, name='dispatch')
class ScriptManagementView(FileManagementView):
    """
    Manage custom scripts
    """
    base_path = settings.SCRIPTS_ROOT
    template_name = 'cloud/scripts.html'

    def _get_scripts(self):
        scripts = get_scripts()

        modules = {}
        for name in self.list_files():
            attrs = os.stat(os.path.join(self.base_path, name))
            mtime = datetime.datetime.fromtimestamp(attrs.st_mtime)
            module_name = f"{name.split('.')[0]}"
            modules[name] = {
                'size': attrs.st_size,
                'mtime': mtime,
                'module': module_name,
                'scripts': scripts.get(module_name, [])
            }

        return modules

    def extra_context(self, request):
        return {
            'scripts': self._get_scripts(),
        }


@method_decorator(superuser_required, name='dispatch')
class ScriptDeleteView(FileDeleteView):
    base_path = settings.SCRIPTS_ROOT
    return_url = 'plugins:cloud:scripts'
