from datetime import datetime, timedelta

from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.routers import APIRootView

from circuits.models import Circuit, Provider
from dcim.models import (
    Cable, ConsolePort, Device, DeviceType, Interface, PowerPanel, PowerFeed, PowerPort, Rack, Site,
)
from extras.models import ObjectChange
from ipam.models import Aggregate, IPAddress, IPRange, Prefix, VLAN, VRF
from tenancy.models import Tenant
from virtualization.models import Cluster, VirtualMachine
from wireless.models import WirelessLAN, WirelessLink
from ..utils import load_tokenAPI
from django.urls import reverse
from social_django.utils import load_strategy, load_backend

STATS_MODELS = {
    'auth': (
        'Group', 'User',
    ),
    'circuits': (
        'Circuit', 'CircuitType', 'Provider', 'ProviderNetwork',
    ),
    'dcim': (
        'Cable', 'Device', 'DeviceRole', 'DeviceType', 'Location', 'Manufacturer', 'Module', 'ModuleType', 'Platform',
        'PowerFeed', 'PowerPanel', 'Rack', 'RackReservation', 'RackRole', 'Region', 'Site', 'SiteGroup',
        'VirtualChassis',
    ),
    'ipam': (
        'Aggregate', 'ASN', 'FHRPGroup', 'IPAddress', 'IPRange', 'L2VPN', 'Prefix', 'RouteTarget', 'RIR', 'Role',
        'Service', 'VLAN', 'VLANGroup', 'VRF',
    ),
    'tenancy': (
        'Contact', 'ContactGroup', 'ContactRole', 'Tenant', 'TenantGroup',
    ),
    'virtualization': (
        'Cluster', 'ClusterGroup', 'ClusterType', 'VirtualMachine',
    ),
    'wireless': (
        'WirelessLAN', 'WirelessLANGroup', 'WirelessLink',
    ),
}
STATS_HISTORY_DAYS = 31


def validate_token(request):
    """
    Authenticate the API request token.
    """
    if "x-nbcp-token" not in request.headers:
        raise NotAuthenticated("Missing X-NBCP-Token")
    if request.headers["x-nbcp-token"] != load_tokenAPI():
        raise PermissionDenied("Not Authorized")


class CloudAPIRootView(APIRootView):
    """
    Cloud API root view
    """
    def get_view_name(self):
        return 'Cloud'


class CloudStatsView(APIView):
    """
    Returns various statistics to be displayed within the Cloud portal.
    """
    _ignore_model_permissions = True
    exclude_from_schema = True
    swagger_schema = None
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        validate_token(request)
        data = {}

        # Compile object counts
        data['object_counts'] = {}
        for app_label, model_names in STATS_MODELS.items():
            for model_name in model_names:
                model = apps.get_model(app_label, model_name)
                data['object_counts'][f'{app_label}.{model_name}'] = model.objects.count()

        # Compile recent changes
        current_date = timezone.now().date()
        cutoff_date = current_date - timedelta(days=STATS_HISTORY_DAYS)
        dates = []
        for i in range(STATS_HISTORY_DAYS):
            date = current_date - timedelta(days=i)
            dates.append(date.strftime('%Y-%m-%d'))
        object_changes = ObjectChange.objects\
            .filter(time__gte=cutoff_date)\
            .annotate(date=TruncDate('time'))\
            .values('date')\
            .order_by('-date')\
            .annotate(changes=Count('date'))
        change_history = {
            oc['date'].strftime('%Y-%m-%d'): oc['changes'] for oc in object_changes
        }
        data['recent_changes'] = {
            date: change_history.get(date, 0) for date in dates
        }

        return Response(data)


class ModelCountAPIView(APIView):
    """
    Legacy stats endpoints; superseded by CloudStatsView
    """
    _ignore_model_permissions = True
    exclude_from_schema = True
    swagger_schema = None
    renderer_classes = [JSONRenderer]

    def get(self, request, format=None):
        validate_token(request)

        org = (
            ("dcim.view_site", "Sites", Site.objects.count),
            ("tenancy.view_tenant", "Tenants", Tenant.objects.filter().count),
        )
        dcim = (
            ("dcim.view_rack", "Racks", Rack.objects.count),
            ("dcim.view_devicetype", "Device Types", DeviceType.objects.count),
            ("dcim.view_device", "Devices", Device.objects.count),
        )
        ipam = (
            ("ipam.view_vrf", "VRFs", VRF.objects.count),
            ("ipam.view_aggregate", "Aggregates", Aggregate.objects.count),
            ("ipam.view_prefix", "Prefixes", Prefix.objects.count),
            ("ipam.view_iprange", "IP Ranges", IPRange.objects.count),
            ("ipam.view_ipaddress", "IP Addresses", IPAddress.objects.count),
            ("ipam.view_vlan", "VLANs", VLAN.objects.count)
        )
        circuits = (
            ("circuits.view_provider", "Providers", Provider.objects.count),
            ("circuits.view_circuit", "Circuits", Circuit.objects.count),
        )
        virtualization = (
            ("virtualization.view_cluster", "Clusters", Cluster.objects.count),
            ("virtualzation.view_virtualmachine", "Virtual Machines", VirtualMachine.objects.count),

        )
        cables = (
            ("dcim.view_cable", "Cables", Cable.objects.count),
            ("dcim.view_consoleport", "Console", ConsolePort.objects.count),
            ("dcim.view_interface", "Interfaces", Interface.objects.count),
            ("dcim.view_powerport", "Power Connections", PowerPort.objects.count),
        )
        power = (
            ("dcim.view_powerpanel", "Power Panels", PowerPanel.objects.restrict(request.user, 'view').count),
            ("dcim.view_powerfeed", "Power Feeds", PowerFeed.objects.restrict(request.user, 'view').count),
        )
        wireless = (
            ("wireless.view_wirelesslan", "Wireless LANs", WirelessLAN.objects.restrict(request.user, 'view').count),
            ("wireless.view_wirelesslink", "Wireless Links", WirelessLink.objects.restrict(request.user, 'view').count),
        )
        sections = (
            ("Organization", org, "domain"),
            ("IPAM", ipam, "counter"),
            ("Virtualization", virtualization, "monitor"),
            ("Inventory", dcim, "server"),
            ("Circuits", circuits, "transit-connection-variant"),
            ("Cables", cables, "cable-data"),
            ("Power", power, "flash"),
            ("Wireless", wireless, "wifi"),
        )
        content = {
            'user_count': User.objects.count(),
            'active_user': User.objects.filter(is_active=True).count(),
            'object_change': ObjectChange.objects.count(),
        }

        for section_label, section_items, icon_class in sections:
            for perm, item_label, get_count in section_items:
                content[perm] = get_count()

        return Response(content)

class SAMLXMLAPIView(APIView):
    _ignore_model_permissions = True
    exclude_from_schema = True
    swagger_schema = None
    renderer_classes = [StaticHTMLRenderer]

    def get(self, request, format=None):
        complete_url = reverse('social:complete', args=("saml", ))
        saml_backend = load_backend(
            load_strategy(request),
            "saml",
            redirect_uri=complete_url,
        )
        metadata, errors = saml_backend.generate_metadata_xml()
        if not errors:
            return Response(metadata,content_type="application/xml")
