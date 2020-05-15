from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'intranet.evaluations'
    verbose_name = _('intranet Evaluations')
