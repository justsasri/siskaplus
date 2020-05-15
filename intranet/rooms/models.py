from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

from ..core.models import BaseModel
from ..core.enums import MaxLength


class Room(BaseModel):
    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    code = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Code'))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Name'))
    building = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Building'))
    capacity = models.PositiveIntegerField(
        default=15,
        validators=[MinValueValidator(1)],
        verbose_name=_('Capacity'))

    # wagtail autocomplete
    autocomplete_search_field = 'name'

    def autocomplete_label(self):
        return "{} | {}".format(self.code, self.name)

    def __str__(self):
        return self.name
