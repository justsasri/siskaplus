from django.db import models
from django.utils import translation
from django.core.validators import MinValueValidator, MaxValueValidator

from polymorphic.models import PolymorphicModel, PolymorphicManager
from django_numerators.models import NumeratorMixin

# Intranet Packages Here

from ...core.models import BaseModel
from ...core.enums import MaxLength, DVCPStatus
from .academic import Course
from .students import Student

_ = translation.gettext_lazy


class ScoreManager(PolymorphicManager):
    def get_queryset(self):
        return super().get_queryset()


class Score(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")

    objects = ScoreManager()

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='course_scores',
        verbose_name=_('Course'))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='scores',
        verbose_name=_("Student"))
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Numeric Score"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("Alphabetic Score"))

    def __str__(self):
        return "{} - {}".format(self.student, self.course)


class StudentScore(Score):
    class Meta:
        verbose_name = _("Student Score")
        verbose_name_plural = _("Student Scores")


class ConversionScore(Score):
    class Meta:
        verbose_name = _("Conversion Score")
        verbose_name_plural = _("Conversion Scores")

    ori_code = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Code'))
    ori_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Name'))
    ori_numeric_score = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_('Origin Numeric'))
    ori_alphabetic_score = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Alphabetic'))


class StudentConversion(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("Student Conversion")
        verbose_name_plural = _("Student Conversions")

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='conversions',
        verbose_name=_("Student"))
    ori_institution_name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Institution Name'),
        help_text=_("Institusi asal"))
    ori_program_study = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Program Study'),
        help_text=_("Program Studi asal"))
    ori_year_of_force = models.PositiveIntegerField(
        default=2010,
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)],
        verbose_name=_('Year of force'),
        help_text=_('Tahun masuk/angkatan pada institusi asal'))
    status = models.CharField(
        max_length=MaxLength.SHORT.value,
        choices=DVCPStatus.CHOICES.value,
        default=DVCPStatus.DRAFT.value,
        verbose_name=_('Status'))

    def __str__(self):
        return str(self.student)


class StudentConversionItem(BaseModel):
    class Meta:
        verbose_name = _("Student Conversion Score")
        verbose_name_plural = _("Student Conversion Scores")

    conversion = models.ForeignKey(
        StudentConversion,
        on_delete=models.PROTECT,
        related_name='conversion_items',
        verbose_name=_('Conversion'))
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='conversion_items',
        verbose_name=_('Course'))
    ori_code = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Code'))
    ori_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Name'))
    ori_numeric_score = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_('Origin Numeric'))
    ori_alphabetic_score = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Alphabetic'))
    numeric = models.DecimalField(
        default=1,
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_("Numeric Score"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("Alphabetic Score"))

    def __str__(self):
        return "%s, %s" % (self.ori_code, self.ori_name)
