from django.db import models
from django.db.utils import cached_property
from django.conf import settings
from django.utils import timezone, translation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.shortcuts import reverse

from django_numerators.models import NumeratorMixin
from django_qrcodes.models import QRCodeMixin

# Intranet Packages Here

from ..core.models import BaseModel
from ..core.enums import MaxLength
from ..academic.enums import StudentStatus
from ..academic.models import (
    CurriculumCourse, AcademicYear, Teacher, Student, Curriculum, Course)
from ..rooms.models import Room
from .enums import LectureType, EnrollmentItemMark, EnrollmentCriteria, LectureStatus, AttendantStatus

_ = translation.gettext_lazy


def add_time(time, duration):
    old_date = timezone.datetime(
        2000, 1, 1, hour=time.hour, minute=time.minute, second=time.second)
    new_date = old_date + timezone.timedelta(minutes=90)
    return new_date.time()


class Lecture(QRCodeMixin, NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("lecture")
        verbose_name_plural = _("lectures")

    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("Teacher"))
    assistant = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='assist_lectures',
        verbose_name=_("assistant"))
    curriculum_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("course"))
    curriculum = models.ForeignKey(
        Curriculum,
        null=True, blank=False,
        on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("curriculum"))
    course = models.ForeignKey(
        Course,
        null=True, blank=False,
        on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("course"))
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='lectures',
        verbose_name=_("academic year"))
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT,
        related_name='lectures',
        verbose_name=_("room"))
    date_start = models.DateField(
        null=True, blank=False,
        verbose_name=_('date start'),
        help_text=_('First schedule.'))
    time_start = models.TimeField(
        default=timezone.now,
        verbose_name=_("time start"))
    duration = models.PositiveIntegerField(
        verbose_name=_('duration'),
        help_text=_("Lecture duration in minutes"))
    series = models.PositiveIntegerField(
        verbose_name=_('series'),
        help_text=_("Total meet up"))
    min_capacity = models.PositiveIntegerField(
        default=15,
        validators=[MinValueValidator(1)],
        verbose_name=_('min capacity'))
    max_capacity = models.PositiveIntegerField(
        default=35,
        validators=[MinValueValidator(1)],
        verbose_name=_('max capacity'))
    status = models.CharField(
        max_length=3,
        choices=LectureStatus.CHOICES.value,
        default=LectureStatus.DRAFT.value,
        verbose_name=_("status"))

    def __str__(self):
        return self.title

    @cached_property
    def title(self):
        return "{} / {}".format(
            self.inner_id,
            str(self.curriculum_course.course)
        )

    @property
    def is_space_available(self):
        return self.get_enrolled_students().count() < self.max_capacity

    @property
    def default_time_end(self):
        return add_time(self.default_time_start, self.duration)

    def get_enrolled_students(self):
        return self.enrollments.select_related('enrollment').filter(enrollment__is_valid=True)

    def get_qrcode_data(self):
        return settings.BASE_URL + self.get_absolute_url()

    def get_absolute_url(self):
        return reverse('classrooms_lecture_inspect', args=(self.id,))

    def pass_requirements(self, student):
        """ check if student has complete course requirements """
        status = True
        remedy_courses = []
        for req in self.curriculum_course.course.requisites.all():
            graduated = student.scores.filter(
                course=req.requisite,
                alphabetic__in=['A', 'B', 'C']
            ).count()
            if not graduated:
                status = False
                remedy_courses.append(req.requisite)
        return status, remedy_courses

    def add_to_plan(self, request):
        """ Add selected lecture to student plan """

        # make sure user's is has a student and at least 1 student set as primary
        student = request.user.primary_student
        if not student:
            msg = _("%s, you can't add lecture to plan, please select your primary student.")
            raise ValidationError(msg % request.user)

        # check student status is active
        if student.status != StudentStatus.ACTIVE.value:
            msg = _("%s, your student status with id %s is %s please select your active student account")
            raise ValidationError(msg % (request.user, student.student_id, student.get_status_display()))

        # Match student curriculum
        if self.curriculum_course.curriculum != student.curriculum:
            msg = _("%s, this is %s lecture, please select lecture that match your curriculum.")
            raise ValidationError(msg % (student, self.curriculum_course.curriculum.name))

        # Check student is fullfilled requirements
        user_passes, required_courses = self.pass_requirements(student)
        if not user_passes:
            msg = _("%s you must graduated %s")
            raise ValidationError(msg % (student, ", ".join([str(c) for c in required_courses])))

        # Check lecture status, new lecture or remedy based on student score
        has_scores = student.scores.filter(student=student, course=self.curriculum_course.course)
        criteria = EnrollmentCriteria.REMEDY.value if has_scores else EnrollmentCriteria.NEW.value

        plan_item, created = StudentPlan.objects.get_or_create(student=student, lecture=self, criteria=criteria)
        return plan_item

    def save(self, *args, **kwargs):
        self.course = self.curriculum_course.course
        self.curriculum = self.curriculum_course.curriculum
        super(Lecture, self).save(*args, **kwargs)


class LectureScoreWeighting(BaseModel):
    class Meta:
        verbose_name = _("score weighting")
        verbose_name_plural = _("score weightings")

    lecture = models.OneToOneField(
        Lecture,
        on_delete=models.CASCADE,
        verbose_name=_("lecture"))
    attendance = models.PositiveIntegerField(
        default=15,
        verbose_name=_("attendance"))
    homework1 = models.PositiveIntegerField(
        default=10,
        verbose_name=_("homework 1"))
    homework2 = models.PositiveIntegerField(
        default=10,
        verbose_name=_("homework 2"))
    quis1 = models.PositiveIntegerField(
        default=10,
        verbose_name=_("quis 1"))
    quis2 = models.PositiveIntegerField(
        default=10,
        verbose_name=_("quis 2"))
    mid_exam = models.PositiveIntegerField(
        default=20,
        verbose_name=_("mid exam"))
    final_exam = models.PositiveIntegerField(
        default=25,
        verbose_name=_("final exam"))

    @property
    def total(self):
        total = (self.attendance
                 + self.homework1
                 + self.homework2
                 + self.quis1
                 + self.quis2
                 + self.mid_exam
                 + self.final_exam)
        return total

    def clean(self):
        if self.total != 100:
            raise ValidationError(_(
                "Please correct all value, total weight must be 100% current total is {}"
            ).format(self.total))

    def __str__(self):
        return str(self.lecture) + ' Score Weighting'


class LectureStudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('student', 'lecture')


class LectureStudent(BaseModel):
    class Meta:
        verbose_name = _("lecture student")
        verbose_name_plural = _("lecture students")
        unique_together = ('lecture', 'student')

    NEW = 'N'
    REPEAT = 'R'
    STATUS = (
        (NEW, _('New')),
        (REPEAT, _('Repeat'))
    )

    objects = LectureStudentManager()

    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE,
        related_name='students',
        verbose_name=_("Lecture"))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='lectures',
        verbose_name=_("Student"))
    status = models.CharField(
        max_length=3, choices=STATUS, default=NEW,
        verbose_name=_("Status"))
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("is public"))

    def __str__(self):
        return ", ".join([str(self.student), str(self.lecture)])


class LectureScheduleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class LectureSchedule(BaseModel):
    class Meta:
        verbose_name = _("lecture schedule")
        verbose_name_plural = _("lecture schedules")

    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name=_("lecture"))
    session = models.PositiveIntegerField(
        default=1, validators=[
            MinValueValidator(1),
            MaxValueValidator(50)],
        verbose_name=_('session'))
    date = models.DateField(
        default=timezone.now,
        verbose_name="date")
    time_start = models.TimeField(
        default=timezone.now,
        verbose_name=_("time start"))
    time_end = models.TimeField(
        default=timezone.now,
        verbose_name=_("time end"))
    room = models.ForeignKey(
        Room,
        related_name='lecture_schedules',
        on_delete=models.PROTECT,
        verbose_name=_("room name"))
    type = models.CharField(
        max_length=3,
        choices=LectureType.CHOICES.value,
        default=LectureType.MEETING.value,
        verbose_name=_("Type"))

    @property
    def status(self):
        list_date = (
            self.date.year, self.date.month, self.date.day)
        scedule_date_start = timezone.make_aware(
            timezone.datetime(
                *list_date,
                hour=self.time_start.hour,
                minute=self.time_start.minute,
                second=self.time_start.second))
        scedule_date_end = timezone.make_aware(
            timezone.datetime(
                *list_date,
                hour=self.time_end.hour,
                minute=self.time_end.minute,
                second=self.time_end.second))
        cond1 = timezone.now() >= scedule_date_start
        cond2 = timezone.now() <= scedule_date_end
        return True if cond1 and cond2 else False

    def __str__(self):
        return ", ".join(
            [str(self.lecture), str(self.session)])


class StudentAttendance(BaseModel):
    class Meta:
        verbose_name = _("Student Attendance")
        verbose_name_plural = _("Student Attendances")
        unique_together = ('schedule', 'student')

    student = models.ForeignKey(
        LectureStudent,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name=_("Student"))
    schedule = models.ForeignKey(
        LectureSchedule,
        on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    status = models.CharField(
        max_length=3,
        choices=[(str(x.value), str(x.name).title()) for x in AttendantStatus],
        default=AttendantStatus.PRESENT.value,
        verbose_name=_("Status"))
    note = models.CharField(
        max_length=MaxLength.LONG.value,
        null=True, blank=True,
        verbose_name=_("Note"))

    def __str__(self):
        return "{} {}".format(self.student, self.schedule)


class TeacherAttendance(BaseModel):
    class Meta:
        verbose_name = _("Teacher Attendance")
        verbose_name_plural = _("Teacher Attendances")
        unique_together = ('schedule', 'teacher')

    schedule = models.ForeignKey(
        LectureSchedule,
        on_delete=models.CASCADE,
        verbose_name=_("Schedule"))
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        verbose_name=_("Teacher"))
    status = models.CharField(
        max_length=3,
        choices=[(str(x.value), str(x.name).title()) for x in AttendantStatus],
        default=AttendantStatus.PRESENT.value,
        verbose_name=_("Status"))
    note = models.CharField(
        max_length=MaxLength.LONG.value,
        null=True, blank=True,
        verbose_name=_("Note"))

    def __str__(self):
        return "{} {}".format(self.teacher, self.schedule)


class StudentPlan(BaseModel):
    class Meta:
        verbose_name = _("Enrollment Plan")
        verbose_name_plural = _("Enrollment Plans")
        unique_together = ('student', 'lecture')

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='enrollment_plans',
        verbose_name=_("Student"))
    lecture = models.ForeignKey(
        Lecture,
        on_delete=models.CASCADE,
        related_name='student_plans',
        verbose_name=_('Lecture'))
    criteria = models.CharField(
        max_length=2,
        choices=[(str(x.value), str(x.name)) for x in EnrollmentCriteria],
        default=EnrollmentCriteria.NEW.value,
        verbose_name=_('Criteria'))

    def __str__(self):
        return "{} {}".format(self.student, self.lecture.inner_id)


class Enrollment(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")

    doc_code = 'KRS'
    revision = models.ForeignKey(
        'self', related_name='revisions',
        on_delete=models.CASCADE,
        verbose_name=_('Enrolment'))
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name=_("Student"))
    coach = models.ForeignKey(
        Teacher, on_delete=models.CASCADE,
        related_name='student_enrollments',
        verbose_name=_("Coach"),
        help_text=_('Student academic coach'))
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='student_enrollments',
        verbose_name=_('Academic Year'))
    note = models.TextField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("Note for coach"))
    coach_review = models.TextField(
        max_length=MaxLength.MEDIUM.value,
        null=True, blank=True,
        verbose_name=_("Coach review"))
    is_submitted = models.BooleanField(
        default=False,
        verbose_name=_('Submitted'),
        help_text=_('Designates whether enrollment is submitted'))
    is_revision = models.BooleanField(
        default=False,
        verbose_name=_('Revision'),
        help_text=_('Designates whether enrollment is revision version'))
    is_valid = models.BooleanField(
        default=False,
        verbose_name=_('Valid'),
        help_text=_('Designates whether enrollment is valid version, this version will added to invoice'))

    def __str__(self):
        return self.doc_code


class EnrollmentItem(BaseModel):
    class Meta:
        verbose_name = _("Enrollment Item")
        verbose_name_plural = _("Enrollment Items")
        unique_together = ('enrollment', 'lecture')

    enrollment = models.ForeignKey(
        Enrollment,
        related_name='lectures',
        on_delete=models.CASCADE,
        verbose_name=_('Enrolment'))
    lecture = models.ForeignKey(
        Lecture,
        related_name='enrollments',
        on_delete=models.CASCADE,
        verbose_name=_('Lecture'))
    criteria = models.CharField(
        max_length=2,
        choices=[(str(x.value), str(x.name)) for x in EnrollmentCriteria],
        default=EnrollmentCriteria.NEW,
        verbose_name=_('Criteria'))
    mark = models.CharField(
        max_length=10,
        choices=EnrollmentItemMark.CHOICES.value,
        default=EnrollmentItemMark.CHECK.value,
        verbose_name=_('Status'))

    def __str__(self):
        return str(self.lecture)
