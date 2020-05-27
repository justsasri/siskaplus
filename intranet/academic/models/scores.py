from django.db import models, transaction
from django.utils import translation
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.shortcuts import reverse

from polymorphic.models import PolymorphicModel, PolymorphicManager
from django_numerators.models import NumeratorMixin

# Intranet Packages Here

from ...core.models import BaseModel
from ...core.enums import MaxLength, DVCPStatus
from .academic import Course
from .students import Student
from .managers import StudentConversionManager
_ = translation.gettext_lazy


class ScoreRange(BaseModel):
    class Meta:
        verbose_name = _("Score Range")
        verbose_name_plural = _("Score Ranges")
        unique_together = ['schema', 'alphabetic']
        ordering = ['schema', 'alphabetic']

    schema = models.PositiveIntegerField(
        choices=(
            (5, 'D3'),
            (7, 'S1'),
            (8, 'S2'),
            (9, 'S3'),
        ),
        default=7,
        verbose_name=_("Alphabetic Score"))
    alphabetic = models.CharField(
        max_length=2,
        choices=(
            ('A', 'A'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B', 'B'),
            ('B-', 'B-'),
            ('C+', 'C+'),
            ('C', 'C'),
            ('C-', 'C-'),
            ('D', 'D'),
            ('E', 'E'),
            ('I', 'I'),
        ),
        verbose_name=_("Alphabetic Score"))
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4),
        ],
        verbose_name=_("Numeric Score"))
    min_point = models.DecimalField(
        default=0,
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Min Point"))
    max_point = models.DecimalField(
        default=1,
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Max Point"))
    predicate = models.CharField(
        max_length=25, unique=True,
        verbose_name=_("Predicate"))

    def __str__(self):
        return "{} ({})".format(self.alphabetic, self.numeric)


class StudentScoreManager(PolymorphicManager):
    def get_queryset(self):
        return super().get_queryset()


class StudentScore(PolymorphicModel, BaseModel):
    class Meta:
        verbose_name = _("Score")
        verbose_name_plural = _("Scores")

    objects = StudentScoreManager()

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='course_scores',
        verbose_name=_('Course'))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='scores',
        verbose_name=_("Student"))
    sks = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name=_("sks"))
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
        verbose_name=_("Numeric"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("Alphabetic"))
    point = models.PositiveIntegerField(
        default=0,
        editable=False,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10),
        ],
        verbose_name=_("point"))

    def __str__(self):
        return "{} - {}".format(self.student, self.course)

    def save(self, *args, **kwargs):
        self.point = self.sks * self.numeric
        super(StudentScore, self).save(*args, **kwargs)


class PlainStudentScore(StudentScore):
    class Meta:
        verbose_name = _("Plain Student Score")
        verbose_name_plural = _("Plain Student Scores")


class ConversionStudentScore(StudentScore):
    class Meta:
        verbose_name = _("Conversion Student Score")
        verbose_name_plural = _("Conversion Student Scores")

    reference = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('reference'))
    ori_code = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Code'))
    ori_name = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Name'))
    ori_numeric = models.PositiveIntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(4),
        ],
        verbose_name=_('Origin Numeric'))
    ori_alphabetic = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Alphabetic'))


class StudentConversion(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("Student Conversion")
        verbose_name_plural = _("Student Conversions")

    objects = StudentConversionManager()

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

    def get_absolute_url(self):
        return reverse('admin:intranet_academic_studentconversion_inspect', args=(self.id,))

    @property
    def is_editable(self):
        return self.status == DVCPStatus.DRAFT.value

    def pass_delete_validation(self):
        return self.is_editable

    def get_deletion_message(self):
        return _("Non draft %s can't be deleted") % self._meta.verbose_name

    def mark_as_draft(self):
        if self.status != DVCPStatus.VALID.value:
            msg = _('Please select canceled %s') % self._meta.verbose_name
            raise ValidationError(msg)
        self.status = DVCPStatus.DRAFT.value
        self.save()

    def mark_as_valid(self):
        if self.status != DVCPStatus.DRAFT.value:
            msg = _('Please select %s draft') % self._meta.verbose_name
            raise ValidationError(msg)
        self.status = DVCPStatus.VALID.value
        self.save()

    def mark_as_posted(self):
        if self.status != DVCPStatus.VALID.value:
            msg = _('Please select valid %s') % self._meta.verbose_name
            raise ValidationError(msg)
        with transaction.atomic():
            scores = []
            for item in self.conversion_items.all():
                # create student score
                score = ConversionStudentScore(
                    reference=item.conversion.inner_id,
                    student=item.conversion.student,
                    course=item.course,
                    sks=item.course.total,
                    numeric=item.numeric,
                    alphabetic=item.alphabetic,
                    point=item.course.total * item.numeric,
                    ori_code=item.ori_code,
                    ori_name=item.ori_name,
                    ori_numeric=item.ori_numeric,
                    ori_alphabetic=item.ori_alphabetic,
                )
                score.save()
            self.status = DVCPStatus.POSTED.value
            self.save()

    def mark_as_canceled(self):
        if self.status != DVCPStatus.POSTED.value:
            msg = _('Please select posted %s') % self._meta.verbose_name
            raise ValidationError(msg)
        with transaction.atomic():
            scores = ConversionStudentScore.objects.filter(reference=self.inner_id)
            scores.delete()
            self.status = DVCPStatus.VALID.value
            self.save()

    def natural_key(self):
        return (self.inner_id,)


class StudentConversionItem(BaseModel):
    class Meta:
        verbose_name = _("Student Conversion Item")
        verbose_name_plural = _("Student Conversion Items")

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
    ori_numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4),
        ],
        verbose_name=_('Origin Numeric'))
    ori_alphabetic = models.CharField(
        max_length=MaxLength.SHORT.value,
        verbose_name=_('Origin Alphabetic'))
    numeric = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(4),
        ],
        verbose_name=_("Numeric Score"))
    alphabetic = models.CharField(
        max_length=1,
        verbose_name=_("Alphabetic Score"))

    def __str__(self):
        return "%s, %s" % (self.ori_code, self.ori_name)
