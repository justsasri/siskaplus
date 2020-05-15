from django.apps import AppConfig as AppConfigBase
from django.utils.translation import gettext_lazy as _


class AppConfig(AppConfigBase):
    name = 'intranet.lectures'
    label = 'intranet_lectures'
    verbose_name = _('Intranet Lectures')
