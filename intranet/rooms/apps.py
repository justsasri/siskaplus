from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'intranet.rooms'
    label = 'intranet_rooms'
    verbose_name = 'Intranet Rooms'
