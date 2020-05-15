from django.db import models
from django.db.utils import cached_property
from django.utils import translation
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

# Intranet Packages Here

from ...core.enums import MaxLength
from ...core.models import BaseModel
from ...accounts.gravatar import get_user_gravatar
from ..enums import ManagementLevel
from .academic import Course, ManagementUnit
from .managers import TeacherManager

_ = translation.gettext_lazy


class Teacher(BaseModel):
    class Meta:
        verbose_name = _('teacher')
        verbose_name_plural = _('teachers')

    objects = TeacherManager()
    account = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name=_("Account"))
    tid = models.CharField(
        unique=True, null=True, blank=False,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('teacher ID'),
        help_text=_('Provide NIDN or Employee ID'))
    rmu = models.ForeignKey(
        ManagementUnit, on_delete=models.PROTECT,
        related_name='teachers',
        verbose_name=_('management unit'),
        help_text=_("Teacher homebase."),
        limit_choices_to={
            'type': ManagementLevel.PROGRAM_STUDY.value
        })
    courses = models.ManyToManyField(
        Course, blank=True,
        related_name='teachers',
        verbose_name=_('courses'))
    is_active = models.BooleanField(
        default=True, verbose_name=_("active status"))

    def __str__(self):
        return self.name

    @cached_property
    def name(self):
        return str(self.account)

    @cached_property
    def get_gravatar_url(self):
        return get_user_gravatar(self.account)

    def get_absolute_url(self):
        return reverse('academic_teacher_inspect', args=(self.id,))

    def natural_key(self):
        natural_key = (self.tid,)
        return natural_key
