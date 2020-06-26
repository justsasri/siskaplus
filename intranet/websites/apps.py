from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'intranet.websites'
    label = 'intranet_websites'