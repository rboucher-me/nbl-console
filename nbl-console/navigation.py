from extras.plugins import PluginMenuItem, PluginMenu

# Dummy permission to effect superuser check
is_superuser = '_.is_superuser'

menu = PluginMenu(
    label='Cloud',
    groups=(
        ('Scripts & Reports', (
            PluginMenuItem(
                link='plugins:cloud:scripts',
                link_text='Custom scripts',
                permissions=[is_superuser]
            ),
            PluginMenuItem(
                link='plugins:cloud:reports',
                link_text='Reports',
                permissions=[is_superuser]
            ),
        )),
        ('Administration', (
            PluginMenuItem(
                link='plugins:cloud:configuration',
                link_text='Configuration',
                permissions=[is_superuser]
            ),
        )),
    ),
    icon_class='mdi mdi-router'
)
