from django.apps import apps
from django.db import models
from django.db.models.functions import Coalesce
from django.utils import translation

from mptt.models import TreeManager

from ...core.managers import count_subquery, cumulative_count_subquery
from ..enums import StudentStatus

_ = translation.gettext_lazy


class AcademicYearManager(models.Manager):
    def get_active(self):
        try:
            return self.filter(is_active=True).first()
        except self.model.DoesNotExist:
            return None


class ManagementUnitManager(TreeManager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)

    def get_summary(self, *args, **kwargs):
        Course = apps.get_model('academic', model_name='Course', require_ready=True)
        Teacher = apps.get_model('teachers', model_name='Teacher', require_ready=True)
        Student = apps.get_model('students', model_name='Student', require_ready=True)

        return self.get_queryset(*args, **kwargs).annotate(
            total_courses=count_subquery(Course, {'is_active': True}),
            total_cum_courses=cumulative_count_subquery(Course, {'is_active': True}),
            total_teachers=count_subquery(Teacher, {'is_active': True}),
            total_cum_teachers=cumulative_count_subquery(Teacher, {'is_active': True}),
            total_students=count_subquery(Student, {'status': 'ACT'}),
            total_cum_students=cumulative_count_subquery(Student, {'status': 'ACT'}),
        )

    def get_with_summary(self, rmu_queryset=None):
        from .academic import Course
        from .teachers import Teacher
        from .students import Student
        if not rmu_queryset:
            rmu_queryset = self.get_queryset()

        return rmu_queryset.annotate(
            total_courses=count_subquery(Course),
            total_cum_courses=cumulative_count_subquery(Course),
            total_teachers=count_subquery(Teacher),
            total_cum_teachers=cumulative_count_subquery(Teacher),
            total_students=count_subquery(Student),
            total_cum_students=cumulative_count_subquery(Student),
        )


class CurriculumManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_active(self, rmu):
        try:
            return self.filter(rmu=rmu, is_active=True)
        except self.model.DoesNotExist:
            return None

    def get_with_summary(self, curriculum_queryset=None):
        """
            Course type:
            m = mandaroty, c = choice, i = interest, r = research
            Course rmu:
            u = university, f = faculty, m = major, p = program study
        """
        # make sure queryset is available
        if not curriculum_queryset:
            curriculum_queryset = self.get_queryset()

        filter_sks_mu = (
                models.Q(curriculum_courses__course__course_type__code=1)
                & models.Q(curriculum_courses__course__rmu__type=1))
        filter_sks_cu = (
                models.Q(curriculum_courses__course__course_type__code=2)
                & models.Q(curriculum_courses__course__rmu__type=1))
        filter_sks_iu = (
                models.Q(curriculum_courses__course__course_type__code=3)
                & models.Q(curriculum_courses__course__rmu__type=1))
        filter_sks_ru = (
                models.Q(curriculum_courses__course__course_type__code=4)
                & models.Q(curriculum_courses__course__rmu__type=1))

        # faculty courses
        filter_sks_mf = (
                models.Q(curriculum_courses__course__course_type__code=1)
                & models.Q(curriculum_courses__course__rmu__type=2))
        filter_sks_cf = (
                models.Q(curriculum_courses__course__course_type__code=1)
                & models.Q(curriculum_courses__course__rmu__type=2))
        filter_sks_if = (
                models.Q(curriculum_courses__course__course_type__code=3)
                & models.Q(curriculum_courses__course__rmu__type=2))
        filter_sks_rf = (
                models.Q(curriculum_courses__course__course_type__code=4)
                & models.Q(curriculum_courses__course__rmu__type=2))

        # major courses
        filter_sks_mm = (
                models.Q(curriculum_courses__course__course_type__code=1)
                & models.Q(curriculum_courses__course__rmu__type=3))
        filter_sks_cm = (
                models.Q(curriculum_courses__course__course_type__code=2)
                & models.Q(curriculum_courses__course__rmu__type=3))
        filter_sks_im = (
                models.Q(curriculum_courses__course__course_type__code=3)
                & models.Q(curriculum_courses__course__rmu__type=3))
        filter_sks_rm = (
                models.Q(curriculum_courses__course__course_type__code=4)
                & models.Q(curriculum_courses__course__rmu__type=3))

        # program courses
        filter_sks_mp = (
                models.Q(curriculum_courses__course__course_type__code=1)
                & models.Q(curriculum_courses__course__rmu__type=4))
        filter_sks_cp = (
                models.Q(curriculum_courses__course__course_type__code=2)
                & models.Q(curriculum_courses__course__rmu__type=4))
        filter_sks_ip = (
                models.Q(curriculum_courses__course__course_type__code=3)
                & models.Q(curriculum_courses__course__rmu__type=4))
        filter_sks_rp = (
                models.Q(curriculum_courses__course__course_type__code=4)
                & models.Q(curriculum_courses__course__rmu__type=4))

        return curriculum_queryset.select_related('rmu').prefetch_related(
            'curriculum_courses'
        ).annotate(
            # university courses
            sks_mu=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_mu), 0),
            sks_cu=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_cu), 0),
            sks_iu=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_iu), 0),
            sks_ru=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_ru), 0),
            sks_tu=models.F('sks_mu') + models.F('sks_cu') + models.F('sks_iu') + models.F('sks_ru'),

            # faculty courses
            sks_mf=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_mf), 0),
            sks_cf=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_cf), 0),
            sks_if=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_if), 0),
            sks_rf=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_rf), 0),
            sks_tf=models.F('sks_mf') + models.F('sks_cf') + models.F('sks_if') + models.F('sks_rf'),

            # major courses
            sks_mm=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_mm), 0),
            sks_cm=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_cm), 0),
            sks_im=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_im), 0),
            sks_rm=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_rm), 0),
            sks_tm=models.F('sks_mm') + models.F('sks_cm') + models.F('sks_im') + models.F('sks_rm'),

            # program courses
            sks_mp=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_mp), 0),
            sks_cp=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_cp), 0),
            sks_ip=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_ip), 0),
            sks_rp=Coalesce(models.Sum('curriculum_courses__course__total', filter=filter_sks_rp), 0),
            sks_tp=models.F('sks_mp') + models.F('sks_cp') + models.F('sks_ip') + models.F('sks_rp'),

            mandatory=models.F('sks_mu') + models.F('sks_mf') + models.F('sks_mm') + models.F('sks_mp'),
            choice=models.F('sks_cu') + models.F('sks_cf') + models.F('sks_cm') + models.F('sks_cp'),
            interest=models.F('sks_iu') + models.F('sks_if') + models.F('sks_im') + models.F('sks_ip'),
            research=models.F('sks_ru') + models.F('sks_rf') + models.F('sks_rm') + models.F('sks_rp'),

            meeting=Coalesce(models.Sum('curriculum_courses__course__meeting'), 0),
            practice=Coalesce(models.Sum('curriculum_courses__course__practice'), 0),
            field_practice=Coalesce(models.Sum('curriculum_courses__course__field_practice'), 0),
            simulation=Coalesce(models.Sum('curriculum_courses__course__simulation'), 0),
            total=(models.F('meeting')
                   + models.F('practice')
                   + models.F('field_practice')
                   + models.F('simulation'))
        )


class CourseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs)


class CurriculumCourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'curriculum', 'course'
        ).prefetch_related(
            'concentration'
        ).annotate(
            name=models.F('course__name'),
            old_code=models.F('course__old_code'),
            type=models.F('course__course_type__name'),
            type_alias=models.F('course__course_type__alias'),
            group=models.F('course__course_group__name'),
            group_alias=models.F('course__course_group__alias'),
            meeting=models.F('course__meeting'),
            practice=models.F('course__practice'),
            field_practice=models.F('course__field_practice'),
            simulation=models.F('course__simulation'),
            total=models.F('course__total')
        )


class TeacherManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_top_teachers(self):
        return self.get_queryset()

    def get_by_natural_key(self, tid):
        return self.get(tid=tid)


class StudentManager(models.Manager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)

    def get_primary(self, user):
        try:
            return self.get(account=user, primary=True)
        except self.model.DoesNotExist:
            return None

    def active(self):
        qs = self.get_queryset().filter(status=StudentStatus.ACTIVE.value)
        return qs


class StudentConversionManager(models.Manager):
    def get_by_natural_key(self, inner_id):
        return self.get(inner_id=inner_id)
