import datetime
import os

from django.conf import settings
from django.utils.decorators import method_decorator
from extras.reports import get_reports

from cloud.decorators import superuser_required
from .generic import FileDeleteView, FileManagementView

__all__ = (
    'ReportDeleteView',
    'ReportManagementView',
)


@method_decorator(superuser_required, name='dispatch')
class ReportManagementView(FileManagementView):
    """
    Manage reports
    """
    base_path = settings.REPORTS_ROOT
    template_name = 'cloud/reports.html'

    def _get_reports(self):
        reports = {
            module: reports for module, reports in get_reports().items()
        }

        modules = {}
        for name in self.list_files():
            attrs = os.stat(os.path.join(self.base_path, name))
            mtime = datetime.datetime.fromtimestamp(attrs.st_mtime)
            module_name = f"{name.split('.')[0]}"
            modules[name] = {
                'size': attrs.st_size,
                'mtime': mtime,
                'module': module_name,
                'reports': reports.get(module_name, [])
            }

        print(modules)

        return modules

    def extra_context(self, request):
        return {
            'reports': self._get_reports(),
        }


@method_decorator(superuser_required, name='dispatch')
class ReportDeleteView(FileDeleteView):
    base_path = settings.REPORTS_ROOT
    return_url = 'plugins:cloud:reports'
