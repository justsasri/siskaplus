from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.formats import base_formats

from ...accounts.admin import UserAdmin
from ..models import (
    CourseRequisite, AcademicYear, SchoolYear, CourseGroup, CourseType, Concentration,
    ManagementUnit, Curriculum, Course, StudentScore, ConversionScore,
    CurriculumCourse, Teacher, Student, StudentConversion, StudentConversionItem)
from ..resources import (
    StudentResource, TeacherResource,
    CourseResource, CurriculumCourseResource,
    StudentScoreResource)
from ..forms import CourseForm, CurriculumForm, CurriculumCourseForm
from .sites import academic_admin


class AcademicYearAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'school_year', 'semester', 'date_start', 'date_registration', 'date_preparation',
        'date_lecture_open', 'date_lecture_end', 'date_completion', 'date_end'
    ]


class ManagementUnitAdmin(admin.ModelAdmin):
    list_filter = ['type']
    search_fields = ['name']
    list_display = ['unit_name', 'code', 'courses', 'students', 'teachers']

    def courses(self, obj):
        return obj.total_cum_courses

    def students(self, obj):
        return obj.total_cum_students

    def teachers(self, obj):
        return obj.total_cum_teachers

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return ManagementUnit.objects.get_with_summary(qs)


class CurriculumCourseInline(admin.TabularInline):
    extra = 0
    form = CurriculumCourseForm
    model = CurriculumCourse
    raw_id_fields = ['course']


class ProgramStudyFilter(admin.SimpleListFilter):
    title = 'Program Study'
    parameter_name = 'rmu__code'

    def lookups(self, request, model_admin):
        return [(rmu.code, rmu.name) for rmu in ManagementUnit.objects.filter(type=4)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(rmu__code=self.value())
        return queryset


class CurriculumAdmin(admin.ModelAdmin):
    form = CurriculumForm
    search_fields = ['name', 'rmu__name']
    list_filter = [ProgramStudyFilter]
    list_select_related = ['rmu']
    list_display = [
        'name',
        'rmu',
        'sks_graduate',
        'mandatory',
        'choice',
        'interest',
        'research',
        'meeting',
        'practice',
        'field_practice',
        'simulation'
    ]
    raw_id_fields = ['rmu']
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'rmu', 'year', 'sks_graduate', 'is_active', 'is_primary', 'is_public')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('summary', 'description'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return Curriculum.objects.get_with_summary(qs)

    def mandatory(self, obj):
        return obj.mandatory

    def choice(self, obj):
        return obj.choice

    def interest(self, obj):
        return obj.interest

    def research(self, obj):
        return obj.research

    def meeting(self, obj):
        return obj.meeting

    def practice(self, obj):
        return obj.practice

    def field_practice(self, obj):
        return obj.field_practice

    def simulation(self, obj):
        return obj.simulation


class CurriculumCourseAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    form = CurriculumCourseForm
    formats = (base_formats.XLSX,)
    resource_class = CurriculumCourseResource
    search_fields = ['course__name', 'curriculum__year']
    list_filter = ['curriculum']
    list_select_related = ['course']
    list_display = ['course_name', 'code', 'curriculum', 'semester_number', 'sks_graduate', 'sks']
    raw_id_fields = ['course', 'curriculum', 'concentration']

    def course_name(self, obj):
        return obj.name

    def code(self, obj):
        return obj.old_code

    def sks(self, obj):
        return obj.total


class CoursePreRequisiteInline(admin.TabularInline):
    extra = 0
    fk_name = 'course'
    model = CourseRequisite
    raw_id_fields = ['requisite']


class CourseAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    form = CourseForm
    formats = (base_formats.XLSX,)
    resource_class = CourseResource
    search_fields = ['name', 'old_code']
    inlines = [CoursePreRequisiteInline]
    raw_id_fields = ['rmu']
    list_select_related = ['rmu', 'course_type', 'course_group']
    list_filter = ['rmu', 'level', 'is_active', 'course_type', 'course_group', 'year_offered']
    list_display = ['old_code', 'name', 'meeting', 'practice', 'field_practice', 'simulation', 'total']
    fieldsets = (
        (None, {
            'fields': ('old_code', 'name', 'rmu', 'course_type', 'course_group',
                       'level', 'year_offered', 'meeting', 'practice', 'field_practice', 'simulation', 'is_active')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('summary', 'description', 'learning_program', 'dictate', 'teaching_material',
                       'practice_program', 'syllabus'),
        }),
    )


class CourseEqualizerAdmin(admin.ModelAdmin):
    search_fields = ['old_course__course__name']
    list_display = ['old_course', 'new_course', 'sks_new_course', 'sks_old_course']


class TeacherInline(admin.TabularInline):
    min_num = 1
    model = Teacher
    list_select_related = ['rmu']
    raw_id_fields = ['rmu']


class TeacherAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    formats = (base_formats.XLSX,)
    resource_class = TeacherResource
    list_display = ['name', 'tid', 'rmu', 'is_active']
    raw_id_fields = ['account']
    search_fields = ['account__first_name', 'tid']
    list_select_related = ['rmu', 'account']
    list_filter = ['rmu']


class StudentAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    formats = (base_formats.XLSX,)
    resource_class = StudentResource
    search_fields = ['account__first_name', 'student_id']
    list_select_related = ['account', 'rmu', 'year_of_force', 'coach', 'curriculum']
    list_filter = ['status', 'year_of_force', 'registration']
    list_display = ['account', 'student_id', 'rmu', 'year_of_force', 'registration', 'status']
    fields = ['account', 'student_id', 'coach', 'rmu', 'curriculum', 'year_of_force', 'semester',
              'registration', 'registration_id', 'status', 'status_note', 'primary']
    raw_id_fields = ['account', 'rmu', 'year_of_force', 'curriculum', 'coach']


class StudentScoreAdmin(ImportExportMixin, ExportActionMixin, admin.ModelAdmin):
    formats = (base_formats.XLSX,)
    resource_class = StudentScoreResource
    search_fields = [
        'course__course__name', 'course__course__inner_id',
        'student__account__first_name', 'student__student_id'
    ]
    raw_id_fields = ['student', 'course']
    list_display = ['student', 'course', 'numeric', 'alphabetic']


class ConversionScoreAdmin(admin.ModelAdmin):
    search_fields = [
        'course__course__name', 'course__course__inner_id',
        'student__account__first_name', 'student__student_id'
    ]
    raw_id_fields = ['student', 'course']
    list_display = ['student', 'course', 'ori_code', 'ori_name', 'ori_numeric_score',
                    'ori_alphabetic_score', 'alphabetic']


class StudentConversionItemInline(admin.StackedInline):
    extra = 0
    min_num = 1
    model = StudentConversionItem
    raw_id_fields = ['course']

class StudentConversionAdmin(admin.ModelAdmin):
    list_display = ['student', 'inner_id', 'created_at']
    list_select_related = ['student']
    inlines = [StudentConversionItemInline]
    raw_id_fields = ['student']


admin.site.register(SchoolYear, admin.ModelAdmin)
admin.site.register(AcademicYear, admin.ModelAdmin)
admin.site.register(CourseType, admin.ModelAdmin)
admin.site.register(CourseGroup, admin.ModelAdmin)
admin.site.register(Concentration, admin.ModelAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(ManagementUnit, ManagementUnitAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(CurriculumCourse, CurriculumCourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StudentScore, StudentScoreAdmin)
admin.site.register(ConversionScore, ConversionScoreAdmin)
admin.site.register(StudentConversion, StudentConversionAdmin)

academic_admin.register(SchoolYear, admin.ModelAdmin)
academic_admin.register(AcademicYear, admin.ModelAdmin)
academic_admin.register(CourseType, admin.ModelAdmin)
academic_admin.register(CourseGroup, admin.ModelAdmin)
academic_admin.register(Concentration, admin.ModelAdmin)
academic_admin.register(Course, CourseAdmin)
academic_admin.register(ManagementUnit, ManagementUnitAdmin)
academic_admin.register(Curriculum, CurriculumAdmin)
academic_admin.register(CurriculumCourse, CurriculumCourseAdmin)
academic_admin.register(Student, StudentAdmin)
academic_admin.register(Teacher, TeacherAdmin)
academic_admin.register(StudentScore, StudentScoreAdmin)
academic_admin.register(ConversionScore, ConversionScoreAdmin)
academic_admin.register(get_user_model(), UserAdmin)
academic_admin.register(StudentConversion, StudentConversionAdmin)