from django.apps import AppConfig as AppConfigBase


class AppConfig(AppConfigBase):
    name = 'intranet.accounts'
    label = 'intranet_accounts'
    verbose_name = 'Intranet Accounts'
