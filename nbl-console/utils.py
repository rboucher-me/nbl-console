import json
import logging
import requests

from django.conf import settings

API_URL = "https://api.cloud.netboxapp.com/v1"

logger = logging.getLogger('netbox.plugins.cloud')


def save_config(data):
    """
    Handle updating configuration parameters on form submission. Makes two API calls:
      1. updateFromNetboxCloud: Update non-plugin config parameters
      2. updateFromNetboxCloudPlugin: Update PLUGINS and PLUGINS_CONFIG
    """
    headers = {
        'Content-Type': 'application/json',
    }
    base_data = {
        'Token': load_tokenAPI(),
        'Instance': settings.DATABASE['NAME'].split('00')[0],
    }

    # Pop plugins list & config from form data. These will be sent during the second
    # API call.
    plugins_data = {
        'Plugins': data.pop('PLUGINS', []),
        'PluginsConfig': data.pop('PLUGINS_CONFIG', {}),
    }

    # Values must be strings 
    for key in data:
        if type(data[key]) == int or type(data[key]) == float:
            data[key] = str(data[key])
        if data[key] == False:
            data[key] = "false"
        if data[key] == True:
            data[key] = "true"

    # API call to update NetBox configuration
    post_data = {
        **base_data,
        'Action': 'updateFromNetboxCloud',
        'Data': json.dumps(data)
    }
    requests.post(API_URL, data=json.dumps(post_data), headers=headers)

    # API call to update plugins
    post_data = {
        **base_data,
        'Action': 'updateFromNetboxCloudPlugin',
        'Data': json.dumps(plugins_data)
    }
    requests.post(API_URL, data=json.dumps(post_data), headers=headers)


def load_tokenAPI():
    return _read_secret("superuser_api_token", settings.DATABASE['PASSWORD'])


# Read secret from file
def _read_secret(secret_name, default=None):
    try:
        f = open('/run/secrets/' + secret_name, 'r', encoding='utf-8')
    except EnvironmentError:
        return default
    else:
        with f:
            return f.readline().strip()
