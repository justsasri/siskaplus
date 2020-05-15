from django.db import models
from django.utils import translation, timezone
from django.contrib.auth import get_user_model

from mptt.models import MPTTModel, TreeForeignKey
from django_numerators.models import NumeratorMixin

from ..core.enums import MaxLength
from ..core.models import BaseModel
from .managers import (
    DepartmentManager,
    EmployeeManager,
    ExtraPositionManager,
    PositionManager)

_ = translation.gettext_lazy


class Department(MPTTModel, BaseModel):
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    objects = DepartmentManager()

    parent = TreeForeignKey(
        'Department', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='downlines',
        verbose_name=_('Upline'))
    code = models.CharField(
        unique=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Code'))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Name'))

    def __str__(self):
        return self.name

    def get_manager_position(self):
        staffs = getattr(self, 'staffs', None)
        return None if not staffs else staffs.filter(is_manager=True).first()

    def get_co_manager_position(self):
        staffs = getattr(self, 'staffs', None)
        return None if not staffs else staffs.filter(is_co_manager=True).first()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Position(MPTTModel, BaseModel):
    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    objects = PositionManager()

    parent = TreeForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='staffs',
        verbose_name=_('Upline'))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('name'))
    department = TreeForeignKey(
        Department, related_name='staffs',
        on_delete=models.PROTECT,
        verbose_name=_('Department'))
    is_manager = models.BooleanField(
        default=False,
        verbose_name=_('Is Manager'))
    is_co_manager = models.BooleanField(
        default=False,
        verbose_name=_('Is Co-Manager'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is Active'))
    employee_required = models.IntegerField(
        default=1,
        verbose_name=_('Employee required'))

    def get_strips(self):
        return '---' * self.level

    def get_active_chairman(self, max_person=5):
        chairmans = getattr(self, 'chairmans', None)
        if not chairmans:
            return None
        if self.is_manager or self.is_co_manager:
            return chairmans.filter(is_active=True).first()
        else:
            return chairmans.filter(is_active=True)[0:max_person]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Employment(BaseModel):
    class Meta:
        verbose_name = _('Employment')
        verbose_name_plural = _('Employments')

    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Name'))
    note = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Note'))

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Employment, self).save(*args, **kwargs)


class Employee(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    doc_code = 'EMP'

    objects = EmployeeManager()

    account = models.OneToOneField(
        get_user_model(),
        limit_choices_to={'is_employee': True},
        on_delete=models.CASCADE,
        verbose_name=_("Account"))
    eid = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Employee ID'))
    position = TreeForeignKey(
        Position,
        related_name='chairmans',
        on_delete=models.PROTECT,
        verbose_name=_('Position'))
    employment = models.ForeignKey(
        Employment, null=True, blank=True,
        on_delete=models.PROTECT,
        verbose_name=_("Employment"))
    date_registered = models.DateField(
        default=timezone.now,
        verbose_name=_('Date registered'))
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"))

    tax_id = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Tax ID'))
    bank_name = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Bank Name'))
    bank_holder_name = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Bank Holder Name'))
    bank_account_id = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Bank Account ID'))

    def __str__(self):
        return str(self.account)

    def natural_key(self):
        natural_key = (self.eid,)
        return natural_key

    def get_anchestors(self, ascending=True):
        return self.position.get_ancestors(ascending=ascending)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class ExtraPosition(BaseModel):
    class Meta:
        verbose_name = _('Chairman')
        verbose_name_plural = _('Chairmans')
        unique_together = ('employee', 'position')

    objects = ExtraPositionManager()

    position = TreeForeignKey(
        Position, on_delete=models.CASCADE,
        related_name='extra_chairmans',
        verbose_name=_("Position"))
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='extra_positions',
        verbose_name=_("Employee"))
    is_active = models.BooleanField(
        default=False, verbose_name=_("Active"))

    def __str__(self):
        return "{}({})".format(self.employee, self.position)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
