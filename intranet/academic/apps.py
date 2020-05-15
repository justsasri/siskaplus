from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'intranet.academic'
    label = 'intranet_academic'
    verbose_name = _("Intranet Academic")
