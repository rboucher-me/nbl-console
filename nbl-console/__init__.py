from extras.plugins import PluginConfig


class AppConfig(PluginConfig):
    name = 'cloud'
    verbose_name = 'NetBox Cloud'
    version = '1.2.0'
    author = 'NetBox Labs'
    base_url = 'cloud'
    min_version = '3.4'
    required_settings = []
    default_settings = {}


config = AppConfig
