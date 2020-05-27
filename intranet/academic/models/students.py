from django.db import models
from django.db.models import Subquery
from django.db.utils import cached_property
from django.utils import translation
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from django_numerators.models import NumeratorReset, NumeratorMixin

# Intranet Packages Here

from ...core.models import BaseModel
from ...core.enums import MaxLength
from ...accounts.models import get_user_gravatar
from ..enums import StudentStatus, ManagementLevel
from .managers import StudentManager
from .academic import ManagementUnit, SchoolYear, Curriculum
from .teachers import Teacher

_ = translation.gettext_lazy


def get_score_status(alpha_score):
    if alpha_score not in ['A', 'B', 'C', 'D']:
        return '-'
    status = {
        'A': 'lulus',
        'B': 'lulus',
        'C': 'lulus',
        'D': 'mengulang',
        'E': 'mengulang'
    }
    return status[alpha_score]


def get_score_classname(alpha_score):
    if alpha_score not in ['A', 'B', 'C', 'D']:
        return ''
    status = {
        'A': 'success',
        'B': 'success',
        'C': 'warning',
        'D': 'danger',
        'E': 'danger'
    }
    return status[alpha_score]


def get_status_classname(status):
    status = {
        'ACT': 'primary',
        'ALM': 'success',
        'DRO': 'danger',
        'MVD': 'danger',
        'MSC': 'warning'
    }
    return status[status]


class Student(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _('student')
        verbose_name_plural = _('students')
        permissions = (
            ('register_student', _('Can Register New Student')),
        )

    zero_fill = 4
    reset_mode = NumeratorReset.FIXED
    objects = StudentManager()

    student_id = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('student ID'))
    registration_id = models.CharField(
        null=True, blank=False,
        max_length=MaxLength.SHORT.value,
        verbose_name=_("registration ID"))
    registration = models.PositiveIntegerField(
        default=1,
        choices=((1, _('reguler').title()), (2, _('transfer').title())),
        verbose_name=_("registration"))
    account = models.ForeignKey(
        get_user_model(),
        limit_choices_to={'is_student': True},
        on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_("Account"))
    year_of_force = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("year of force"))
    coach = models.ForeignKey(
        Teacher,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='students',
        verbose_name=_('coach'))
    rmu = models.ForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        verbose_name=_('program study'),
        limit_choices_to={
            'type': ManagementLevel.PROGRAM_STUDY.value
        })
    curriculum = models.ForeignKey(
        Curriculum,
        on_delete=models.PROTECT,
        verbose_name=_('curriculum'),
        help_text=_('Student curriculum, important to maintain alumni curriculum'))
    semester = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Semester'),
        help_text=_('Student semester number, updated automatically when student create enrollment document '))
    primary = models.BooleanField(
        default=False, verbose_name=_('primary'),
        help_text=_('Mark as primary student object, used when login'))
    status = models.CharField(
        choices=StudentStatus.CHOICES.value,
        default=StudentStatus.ACTIVE.value,
        max_length=MaxLength.SHORT.value,
        verbose_name=_('status'))
    status_note = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('status note'))

    @cached_property
    def name(self):
        return str(self.account)

    def __str__(self):
        return self.name

    def get_doc_prefix(self):
        form = [
            str(self.year_of_force.year_start)[2:4],
            self.rmu.number,
            self.registration
        ]
        doc_prefix = '{}{}{}'.format(*form)
        return doc_prefix

    def format_inner_id(self):
        form = [
            self.get_doc_prefix(),
            self.format_number()
        ]
        self.inner_id = '{}{}'.format(*form)
        return self.inner_id

    def set_as_primary(self):
        old_primary = Student.objects.get_primary(self.account)
        if old_primary:
            old_primary.primary = False
            old_primary.save()
        self.primary = True
        self.save()
        return True

    def course_max_score_subquery(self, field):
        from .scores import StudentScore
        filter_fields = {
            'student': self,
            'course_id': models.OuterRef('course_id')
        }
        sqs = Subquery(
            StudentScore.objects.filter(
                **filter_fields
            ).only(
                'sks', 'point', 'numeric', 'alphabetic'
            ).order_by('-numeric').values(field)[:1],
            output_field=models.CharField()
        )
        return sqs

    def get_scores(self, semester=None):
        courses = self.curriculum.curriculum_courses.all()
        if semester:
            courses = courses.filter(semester_number=semester)
        scores = courses.annotate(
            alphabetic=self.course_max_score_subquery('alphabetic'),
            numeric=self.course_max_score_subquery('numeric'),
            sks=self.course_max_score_subquery('sks'),
            point=self.course_max_score_subquery('point'),
        )
        return scores

    def get_scores_summary(self, scores):
        summary = scores.aggregate(
            course_remedy=models.Count('id', filter=models.Q(numeric__gt='C')),
            course_graduate=models.Count('id', filter=models.Q(numeric__lte='C')),
            course_total=models.Count('id', filter=models.Q(alphabetic__isnull=False)),
            sks_remedy=models.Sum('sks', filter=models.Q(alphabetic__gt='C')),
            sks_graduate=models.Sum('sks', filter=models.Q(alphabetic__lte='C')),
            sks_total=models.Sum('sks', filter=models.Q(alphabetic__isnull=False)),
            total_point=models.Sum('point', filter=models.Q(alphabetic__isnull=False)),
        )
        summary['ips'] = summary['total_point'] / summary['sks_total']
        return summary

    def get_gravatar_url(self):
        return get_user_gravatar(self.account)

    def get_absolute_url(self):
        return reverse('admin:intranet_academic_student_inspect', args=(self.id,))

    def get_public_url(self):
        return reverse('academic_student_inspect', args=(self.id,))

    def natural_key(self):
        natural_key = (self.student_id,)
        return natural_key

    def enrollment_plans_total_credit(self):
        return self.enrollment_plans.aggregate(
            total=models.Sum('lecture__curriculum_course__course__total')
        )['total'] or 0
