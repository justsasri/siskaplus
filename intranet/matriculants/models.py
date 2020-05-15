from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

from django_personals.models import PersonMinimalAbstract


class Matriculant(PersonMinimalAbstract):
    class Meta:
        verbose_name = _('matriculant')
        verbose_name_plural = _('matriculants')

    account = models.OneToOneField(
        get_user_model(),
        null=True, blank=True,
        related_name='matriculant',
        on_delete=models.CASCADE,
        verbose_name=_('Account'))
