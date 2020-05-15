from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'intranet.matriculants'
    label = 'intranet_matriculants'
    verbose_name = 'Intranet Matriculants'
