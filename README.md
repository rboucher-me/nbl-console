# netbox-cloud-plugin

A NetBox plugin developed by NS1 for its NetBox Cloud product.

This project contains proprietary code - **not for public release.**

## Configuration

1. Create a file `config.json` in the `netbox/netbox/` directory (alongside `configuration.py`) to hold the Cloud-specific configuration parameters. These are the items which can be modified via the plugin's "Configuration" control panel. This file must be writable by the NetBox system user.

2. Enable the `cloud` plugin in NetBox's configuration file (`configuration.py`):

```python
PLUGINS = [
    'cloud',
    # ...
]
```

3. Add the following snippet at the end of `configuration.py`:

```python
# Populate NetBox Cloud configuration file
from cloud.utils import load_config
globals().update(load_config('config.json'))
```

This will automatically populate configuration parameters from the `config.json` file at init time. Note that any parameters which appear in `configuration.py` _after_ the call to `load_config()` will overwrite these values.

4. To enable auto-reload of the NetBox service upon modification of static configuration parameters, add the following to the Gunicorn configuration file:

```python
reload = True
reload_engine = 'inotify'
reload_extra_files = ['/opt/netbox/netbox/config.json']
```
