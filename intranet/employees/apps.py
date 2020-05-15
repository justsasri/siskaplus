from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'intranet.employees'
    label = 'intranet_employees'
    verbose_name = _("Intranet Employees")
