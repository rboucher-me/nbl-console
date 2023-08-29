# Time & date
DATE_FORMAT_CHOICES = (
    ('', 'Default'),
    ('F j, Y', 'December 31, 2021'),
    ('M j, Y', 'Dec 31, 2021'),
    ('j F Y', '31 December 2021'),
    ('j M Y', '31 Dec 2021'),
    ('Y-m-d', '2021-12-31'),
)

SHORT_DATE_FORMAT_CHOICES = (
    ('', 'Default'),
    ('Y-m-d', '2021-12-31'),
    ('m/d/y', '12/31/21'),
    ('m/d/Y', '12/31/2021'),
    ('d/m/y', '31/12/21'),
    ('d/m/Y', '31/12/2021'),
)

TIME_FORMAT_CHOICES = (
    ('', 'Default'),
    ('g:i:s a', '11:59:59 p.m.'),
    ('g:i:s A', '11:59:59 PM'),
    ('G:i:s', '23:59:59'),
)

SHORT_TIME_FORMAT_CHOICES = (
    ('', 'Default'),
    ('G:i', '23:59'),
    ('g:i A', '11:59 PM'),
)

# Authentication
AUTH_BACKEND_AZUREAD = 'social_core.backends.azuread.AzureADOAuth2'
AUTH_BACKEND_OKTA_OIDC = 'social_core.backends.okta_openidconnect.OktaOpenIdConnect'
AUTH_BACKEND_CHOICES = (
    (None, 'None (Disabled)'),
    (AUTH_BACKEND_AZUREAD, 'Microsoft Azure AD'),
    (AUTH_BACKEND_OKTA_OIDC, 'Okta (OIDC)'),
)

# Plugins
PLUGIN_CHOICES = (
    ('netbox_bgp', 'netbox-bgp'),  # k01ek/netbox-bgp
    ('netbox_dns', 'netbox-dns'),  # auroraresearchlab/netbox-dns
    ('netbox_qrcode', 'netbox-qrcode'),  # k01ek/netbox-qrcode
    ('netbox_secretstore', 'netbox-secretstore'),  # DanSheps/netbox-secretstore
    ('netbox_topology_views', 'netbox-topology-views'),  # mattieserver/netbox-topology-views
)
