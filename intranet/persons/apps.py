from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'intranet.persons'
    label = 'intranet_persons'
    verbose_name = 'Intranet Persons'
