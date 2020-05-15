from django.db import models
from django.utils import translation

from polymorphic.models import PolymorphicModel
from mptt.models import TreeForeignKey
from django_numerators.models import NumeratorMixin

from ..core.models import BaseModel
from ..lectures.models import Lecture
from ..employees.models import Employee, Position

_ = translation.ugettext_lazy


class Contract(PolymorphicModel, NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _('contract')
        verbose_name_plural = _('contracts')

    date_start = models.DateField(
        verbose_name=_('start date'))
    date_end = models.DateField(
        verbose_name=_('start date'))


class StructuralContract(Contract):
    class Meta:
        verbose_name = _('structural contract')
        verbose_name_plural = _('sturctural contracts')

    position = TreeForeignKey(
        Position, on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name=_("Position"))
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name=_("Employee"))


class TeacherContract(Contract):
    class Meta:
        verbose_name = _('functional contract')
        verbose_name_plural = _('functional contracts')

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name=_("Employee"))


class TaskForceContract(Contract):
    class Meta:
        verbose_name = _('taskforce contract')
        verbose_name_plural = _('taskforce contracts')

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name=_("Employee"))


class LectureContract(Contract):
    class Meta:
        verbose_name = _('lecture contract')
        verbose_name_plural = _('lecture contracts')

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name=_("Lecture"))
