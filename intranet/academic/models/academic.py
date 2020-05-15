from django.db import models
from django.db.utils import cached_property
from django.utils import translation
from django.shortcuts import reverse

from mptt.models import MPTTModel, TreeForeignKey
from django_numerators.models import NumeratorReset, NumeratorMixin

# Intranet Packages Here

from ...core.models import BaseModel
from ...core.enums import MaxLength
from ..enums import ManagementLevel, Semester, KKNILevel
from .managers import ManagementUnitManager, CurriculumManager, CourseManager, CurriculumCourseManager

_ = translation.gettext_lazy


class ManagementUnit(MPTTModel, BaseModel):
    class Meta:
        verbose_name = _("management unit")
        verbose_name_plural = _("management units")

    objects = ManagementUnitManager()

    type = models.IntegerField(
        default=ManagementLevel.UNIVERSITY.value,
        choices=ManagementLevel.CHOICES.value,
        verbose_name=_("type"))
    parent = TreeForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='childrens',
        verbose_name=_('parent'))
    number = models.CharField(
        max_length=3,
        null=True, blank=True,
        verbose_name=_("number"))
    code = models.SlugField(
        unique=True,
        max_length=3,
        verbose_name=_("code"))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.code,)

    def unit_name(self):
        return "{} {}".format('---' * self.level, self.name)


class Concentration(BaseModel):
    class Meta:
        verbose_name = _("concentration")
        verbose_name_plural = _("concentrations")

    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='concentrations',
        verbose_name=_("Program Study"),
        help_text=_("Management Unit"),
        limit_choices_to={
            'type': ManagementLevel.PROGRAM_STUDY.value
        },
    )
    code = models.SlugField(
        unique=True,
        null=True,
        blank=True,
        max_length=3,
        verbose_name=_("code"))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_("Name"))

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.code,)


class SchoolYear(BaseModel):
    class Meta:
        verbose_name = _("school year")
        verbose_name_plural = _("school years")

    def create_code(self):
        return "{}/{}".format(self.year_start, self.year_end)

    code = models.CharField(
        unique=True, editable=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    year_start = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2030)],
        default=2019,
        verbose_name=_("year start"))
    year_end = models.IntegerField(
        choices=[(x, str(x)) for x in range(2010, 2030)],
        default=2020,
        verbose_name=_("year end"))

    def __str__(self):
        return self.code

    def natural_key(self):
        return (self.code,)

    def save(self, *args, **kwargs):
        self.code = self.create_code()
        super().save(*args, **kwargs)


class AcademicYear(BaseModel):
    class Meta:
        verbose_name = _("academic year")
        verbose_name_plural = _("academic years")

    code = models.CharField(
        unique=True, editable=False,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    semester = models.PositiveIntegerField(
        default=Semester.ODD.value,
        choices=Semester.CHOICES.value,
        verbose_name=_('semester'))
    date_start = models.DateField(
        null=True, blank=False,
        verbose_name=_("date start"),
        help_text=_('Academic start date'))
    date_registration = models.DateField(
        null=True, blank=False,
        verbose_name=_('registration date'),
        help_text=_('Registration open date'))
    date_preparation = models.DateField(
        null=True, blank=False,
        verbose_name=_('preparation date'),
        help_text=_('Admin or staff preparing lecture and schedule.'))
    date_lecture_open = models.DateField(
        null=True, blank=False,
        verbose_name=_('lecture start date'),
        help_text=_('Student start to learn.'))
    date_lecture_close = models.DateField(
        null=True, blank=False,
        verbose_name=_('lecture end date'),
        help_text=_('Lecture activity ended, teacher complete required report and score .'))
    date_completion = models.DateField(
        null=True, blank=False,
        verbose_name=_('date completion'),
        help_text=_('Lecture closed forever.'))
    date_end = models.DateField(
        null=True, blank=False,
        verbose_name=_("date end"),
        help_text=_('Academic end'))
    school_year = models.ForeignKey(
        SchoolYear, on_delete=models.PROTECT,
        verbose_name=_("school year"))

    def __str__(self):
        return self.code

    def natural_key(self):
        return (self.code,)

    def save(self, *args, **kwargs):
        self.code = "{} S{}".format(self.school_year, self.semester)
        super().save(*args, **kwargs)


class CourseType(BaseModel):
    class Meta:
        verbose_name = _("course type")
        verbose_name_plural = _("course types")
        ordering = ('code',)

    code = models.PositiveIntegerField(
        unique=True, default=1,
        choices=[(x, str(x)) for x in range(1, 10)],
        verbose_name=_("code"))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_("name"))
    alias = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_("alias"))

    def __str__(self):
        return "{}".format(self.name)

    def natural_key(self):
        return (self.code,)


class CourseGroup(BaseModel):
    class Meta:
        verbose_name = _("course group")
        verbose_name_plural = _("course groups")
        ordering = ('code',)

    code = models.PositiveIntegerField(
        unique=True, default=1,
        choices=[(x, str(x)) for x in range(1, 10)],
        verbose_name=_("Code"))
    name = models.CharField(
        max_length=MaxLength.LONG.value,
        verbose_name=_("Name"))
    alias = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.LONG.value,
        verbose_name=_("Alias"))

    def __str__(self):
        return "{}".format(self.name)

    def natural_key(self):
        return (self.code,)


class Course(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")
        ordering = ('inner_id',)

    zero_fill = 2
    objects = CourseManager()
    reset_mode = NumeratorReset.FIXED

    # Deprecated
    old_code = models.CharField(
        null=True, blank=False,
        unique=True,  # Force Unique, current natural key
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"),
        help_text=_('Maintain legacy system data integrity'))

    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    level = models.PositiveIntegerField(
        choices=KKNILevel.UNIVERSITY.value,
        default=KKNILevel.S1.value,
        verbose_name=_('level'))
    year_offered = models.PositiveIntegerField(
        choices=[(x, str(x)) for x in range(1, 5)], default=1,
        verbose_name=_('year offered'))
    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='courses',
        verbose_name=_("management unit"))
    course_type = models.ForeignKey(
        CourseType,
        related_name='courses',
        on_delete=models.PROTECT,
        verbose_name=_("course type"))
    course_group = models.ForeignKey(
        CourseGroup,
        related_name='courses',
        on_delete=models.PROTECT,
        verbose_name=_("course group"))
    summary = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("summary"))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_("description"))
    meeting = models.PositiveIntegerField(
        default=0, verbose_name=_("Meeting"))
    practice = models.PositiveIntegerField(
        default=0, verbose_name=_("Practice"))
    field_practice = models.PositiveIntegerField(
        default=0, verbose_name=_("Field"))
    simulation = models.PositiveIntegerField(
        default=0, verbose_name=_("Simulation"))
    total = models.PositiveIntegerField(
        editable=False, default=0,
        verbose_name=_("Total"))
    learning_program = models.URLField(
        null=True, blank=True,
        verbose_name=_("learning program"),
        help_text=_('Lecture Program Unit a.k.a SAP'))
    dictate = models.URLField(
        null=True, blank=True,
        verbose_name=_("dictate"))
    teaching_material = models.URLField(
        null=True, blank=True,
        verbose_name=_("teaching material"))
    practice_program = models.URLField(
        null=True, blank=True,
        verbose_name=_("practice program"))
    syllabus = models.URLField(
        null=True, blank=True,
        verbose_name=_("syllabus"))
    is_active = models.BooleanField(
        default=True, verbose_name=_("active status"))
    is_public = models.BooleanField(
        default=True, verbose_name=_('Public'))

    @cached_property
    def has_lpu(self):
        return bool(self.learning_program)

    @cached_property
    def has_dictate(self):
        return bool(self.dictate)

    @cached_property
    def has_teaching_material(self):
        return bool(self.teaching_material)

    @cached_property
    def has_practice_program(self):
        return bool(self.practice_program)

    @property
    def course_code(self):
        # TODO deprecation, inner_id nextime
        return self.old_code

    @property
    def prerequisite(self):
        req = ", ".join([str(i.requisite.name) for i in self.get_requisite()])
        return req

    def __str__(self):
        return "{}, {}".format(self.course_code, self.name)

    def natural_key(self):
        return (self.old_code,)

    def get_requisite(self):
        prerequesite = getattr(self, 'requisites', None)
        return [] if not prerequesite else prerequesite.all()

    def get_doc_prefix(self):
        form = [self.rmu.code, self.course_type.code, self.course_group.code]
        doc_prefix = '{}{}{}'.format(*form)
        return doc_prefix

    def format_inner_id(self):
        """ Inner ID final format """
        form = [
            self.get_doc_prefix(),
            self.level,
            self.year_offered,
            self.format_number()
        ]
        self.inner_id = '{}{}{}{}'.format(*form)
        return self.inner_id

    def get_teachers(self):
        teachers = getattr(self, 'teachers', None)
        return [] if not teachers else teachers.all()

    def save(self, **kwargs):
        self.total = (
                self.meeting
                + self.practice
                + self.field_practice
                + self.simulation
        )
        super().save(**kwargs)

    def get_absolute_url(self):
        return reverse('academic_course_inspect', args=(self.id,))


class CourseRequisite(BaseModel):
    class Meta:
        verbose_name = _("Course prerequisite")
        verbose_name_plural = _("Course prerequisite")

    SCORE = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    )
    course = models.ForeignKey(
        Course,
        related_name="requisites",
        on_delete=models.CASCADE,
        verbose_name=_("course"))
    requisite = models.ForeignKey(
        Course, null=True, blank=True,
        related_name="required_by",
        on_delete=models.CASCADE,
        verbose_name=_("requisite"))
    score = models.CharField(
        max_length=2, default='C', choices=SCORE,
        verbose_name=_('min graduated score'))

    def __str__(self):
        return ", ".join([str(self.course.name), str(self.requisite.name)])


class Curriculum(BaseModel):
    class Meta:
        verbose_name = _("Curriculum")
        verbose_name_plural = _("Curriculums")

    objects = CurriculumManager()

    rmu = TreeForeignKey(
        ManagementUnit,
        on_delete=models.PROTECT,
        related_name='curriculums',
        verbose_name=_("Program Study"),
        help_text=_("Management Unit"),
        limit_choices_to={'type': ManagementLevel.PROGRAM_STUDY.value})
    code = models.CharField(
        unique=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("code"))
    year = models.CharField(
        max_length=4,
        choices=[(str(x), str(x)) for x in range(2010, 2030)],
        default='2019',
        verbose_name=_("year"))
    name = models.CharField(
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("name"))
    sks_graduate = models.PositiveIntegerField(
        default=0,
        verbose_name=_("SKS graduate"))
    summary = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_("summary"))
    description = models.TextField(
        null=True, blank=True,
        max_length=MaxLength.RICHTEXT.value,
        verbose_name=_("description"))
    is_active = models.BooleanField(
        default=True, verbose_name=_('active'))
    is_public = models.BooleanField(
        default=True, verbose_name=_('public'))
    is_primary = models.BooleanField(
        verbose_name=_('primary'),
        default=False)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.code,)

    def create_code(self):
        self.code = "".join([self.rmu.code, self.year[-2:]])

    def save(self, *args, **kwargs):
        self.create_code()
        super().save(*args, **kwargs)

    def set_as_primary(self):
        old_primary = Curriculum.objects.get_primary(self.rmu)
        if old_primary:
            old_primary.primary = False
            old_primary.save()
        self.is_primary = True
        self.save()

    def activate(self):
        self.is_active = True
        self.save()

    def get_summary(self):
        return Curriculum.objects.get_with_summary().get(pk=self.id)

    def get_absolute_url(self):
        return reverse('academic_curriculum_inspect', args=(self.id,))

    def get_curriculum_courses_items(self):
        values = [
            'id', 'course__id', 'name', 'old_code', 'type', 'group', 'type_alias', 'group_alias',
            'meeting', 'practice', 'field_practice', 'simulation', 'total',
            'concentration__code', 'semester_number',
        ]
        return self.curriculum_courses.all().values(*values)

    def get_courses_by_semester(self):
        semester = []
        semester_list = []
        curriculum_courses = self.get_curriculum_courses_items()
        for course in curriculum_courses:
            if course['semester_number'] not in semester:
                semester.append(course['semester_number'])
        for sms in semester:
            current_courses = [course for course in curriculum_courses if course['semester_number'] == sms]
            semester_list.append({
                'number': sms,
                'course_count': len(current_courses) or 0,
                'meeting': sum(map(lambda x: x['meeting'], current_courses)),
                'practice': sum(map(lambda x: x['practice'], current_courses)),
                'field_practice': sum(map(lambda x: x['field_practice'], current_courses)),
                'simulation': sum(map(lambda x: x['simulation'], current_courses)),
                'total': sum(map(lambda x: x['total'], current_courses)),
                'curriculum_courses': current_courses
            })
        return semester_list


class CurriculumCourse(NumeratorMixin, BaseModel):
    class Meta:
        verbose_name = _("curricullum course")
        verbose_name_plural = _("curricullum courses")
        unique_together = ('curriculum', 'course')
        ordering = ('curriculum', 'semester_number',)

    zero_fill = 2
    objects = CurriculumCourseManager()

    curriculum = models.ForeignKey(
        Curriculum, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("curriculum"))
    semester_number = models.PositiveIntegerField(
        default=1, null=True, blank=True,
        choices=[(x, str(x)) for x in range(1, 9)],
        verbose_name=_('semester'))
    sks_graduate = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name=_('SKS graduate'),
        help_text=_('Minimum sks graduated to enroll this course'))
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE,
        related_name='curriculum_courses',
        verbose_name=_("course"))
    concentration = models.ManyToManyField(
        Concentration, blank=True,
        related_name='curriculum_courses',
        verbose_name=_("concentration"))

    def __str__(self):
        return str(self.course.name)

    def get_doc_prefix(self):
        form = [self.curriculum.code, self.semester_number]
        doc_prefix = '{}{}'.format(*form)
        return doc_prefix

    def format_inner_id(self):
        """ Inner ID final format """
        form = [
            self.get_doc_prefix(),
            self.format_number()
        ]
        self.inner_id = '{}{}'.format(*form)
        return self.inner_id

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CourseEqualizer(BaseModel):
    class Meta:
        verbose_name = _("course equalizer")
        verbose_name_plural = _("course equalizers")
        unique_together = ('old_course', 'new_course')

    old_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='old_equalizers',
        verbose_name=_('old course'))
    sks_old_course = models.IntegerField(
        verbose_name=_('SKS old'))
    new_course = models.ForeignKey(
        CurriculumCourse,
        on_delete=models.PROTECT,
        related_name='new_equalizers',
        verbose_name=_('New Course'))
    sks_new_course = models.IntegerField(
        verbose_name=_('SKS new'))

    def __str__(self):
        return "{}-{}".format(self.old_course, self.new_course)
