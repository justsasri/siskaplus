from import_export.resources import ModelResource
from import_export import widgets, fields
from import_export.fields import Field
from django.contrib.auth import get_user_model

from ..core.resource_widgets import UUIDWidget
from .models import (
    Student, Teacher, SchoolYear, ManagementUnit, Curriculum, Course, CurriculumCourse,
    CourseType, CourseGroup, StudentScore, StudentConversion, StudentConversionItem,
    Concentration
)


class StudentResource(ModelResource):
    class Meta:
        model = Student
        fields = (
            'id', 'account', 'student_id', 'registration_id', 'registration', 'year_of_force', 'coach', 'rmu',
            'curriculum', 'semester', 'primary', 'status', 'status_note'
        )

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    name = Field(column_name='name', readonly=True)
    student_id = Field(column_name='npm', attribute='student_id')
    account = fields.Field(
        column_name='email_account',
        attribute='account',
        widget=widgets.ForeignKeyWidget(get_user_model(), 'email'))
    year_of_force = fields.Field(
        column_name='angkatan',
        attribute='year_of_force',
        widget=widgets.ForeignKeyWidget(SchoolYear, 'code'))
    coach = fields.Field(
        column_name='pembimbing_akademik',
        attribute='coach',
        widget=widgets.ForeignKeyWidget(Teacher, 'tid'))
    rmu = fields.Field(
        column_name='program_studi',
        attribute='rmu',
        widget=widgets.ForeignKeyWidget(ManagementUnit, 'code'))
    curriculum = fields.Field(
        column_name='kurikulum',
        attribute='curriculum',
        widget=widgets.ForeignKeyWidget(Curriculum, 'code'))

    def dehydrate_name(self, obj):
        account = getattr(obj, 'account', None)
        return '%s' % account


class TeacherResource(ModelResource):
    class Meta:
        model = Teacher
        fields = (
            'id', 'account', 'tid', 'rmu', 'courses', 'is_active'
        )

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    name = Field(column_name='name', readonly=True)
    tid = Field(column_name='nidn', attribute='tid')
    account = fields.Field(
        column_name='email_account',
        attribute='account',
        widget=widgets.ForeignKeyWidget(get_user_model(), 'email'))
    rmu = fields.Field(
        column_name='program_studi',
        attribute='rmu',
        widget=widgets.ForeignKeyWidget(ManagementUnit, 'code'))
    courses = fields.Field(
        column_name='mata_kuliah',
        attribute='courses',
        widget=widgets.ManyToManyWidget(Course, separator=',', field='old_code'))

    def dehydrate_name(self, obj):
        account = getattr(obj, 'account', None)
        return '%s' % account


class CourseResource(ModelResource):
    class Meta:
        model = Course
        exclude = ('created_at', 'reg_number', 'inner_id')

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    rmu = fields.Field(
        column_name='manajemen_unit',
        attribute='rmu',
        widget=widgets.ForeignKeyWidget(ManagementUnit, 'code'))
    course_type = fields.Field(
        column_name='jenis_mk',
        attribute='course_type',
        widget=widgets.ForeignKeyWidget(CourseType, 'alias'))
    course_group = fields.Field(
        column_name='kelompok_mk',
        attribute='course_group',
        widget=widgets.ForeignKeyWidget(CourseGroup, 'alias'))


class CurriculumCourseResource(ModelResource):
    class Meta:
        model = CurriculumCourse
        exclude = ('created_at', 'reg_number', 'inner_id')

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    semester_number = Field(
        column_name='semester',
        attribute='semester_number')
    curriculum = fields.Field(
        column_name='kurikulum',
        attribute='curriculum',
        widget=widgets.ForeignKeyWidget(Curriculum, 'code'))
    course = fields.Field(
        column_name='mata_kuliah',
        attribute='course',
        widget=widgets.ForeignKeyWidget(Course, 'old_code'))
    name = Field(column_name='nama_mk', readonly=True)
    concentration = fields.Field(
        column_name='konsentrasi',
        attribute='concentration',
        widget=widgets.ManyToManyWidget(
            Concentration, separator=',', field='code'))
    sks_graduate = Field(
        column_name='min_sks_lulus',
        attribute='sks_graduate')

    def dehydrate_name(self, obj):
        course = getattr(obj, 'course', None)
        return '%s' % '' if not course else str(course.name)


class StudentScoreResource(ModelResource):
    class Meta:
        model = StudentScore
        exclude = ('created_at', 'score_ptr', 'polymorphic_ctype')

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    student = fields.Field(
        column_name='npm',
        attribute='student',
        widget=widgets.ForeignKeyWidget(Student, 'student_id'))
    student_name = Field(column_name='nama_mhs', readonly=True)
    course = fields.Field(
        column_name='kode_mk',
        attribute='course',
        widget=widgets.ForeignKeyWidget(Course, 'old_code'))
    course_name = Field(column_name='nama_mk', readonly=True)

    def dehydrate_student_name(self, obj):
        student = getattr(obj, 'student', None)
        return '%s' % '' if not student else str(student)

    def dehydrate_course_name(self, obj):
        course = getattr(obj, 'course', None)
        return '%s' % '' if not course else str(course.name)


class StudentConversionItemResource(ModelResource):
    class Meta:
        model = StudentConversionItem
        exclude = ('created_at', 'studentscore_ptr', 'polymorphic_ctype',
                   'is_trash', 'trashed_by', 'trashed_at')

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    conversion = fields.Field(
        column_name='conversion',
        attribute='conversion',
        widget=widgets.ForeignKeyWidget(StudentConversion, 'inner_id'))
    course = fields.Field(
        column_name='mata_kuliah',
        attribute='course',
        widget=widgets.ForeignKeyWidget(Course, 'old_code'))