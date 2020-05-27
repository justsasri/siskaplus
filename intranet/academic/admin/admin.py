from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.formats import base_formats

from ...admin.admin import ModelAdmin
from ..models import *
from ..resources import (
    CourseResource,
    StudentResource,
    TeacherResource,
    StudentConversionItemResource,
    CurriculumCourseResource)
from ..forms import (
    CourseForm,
    CurriculumForm,
    CurriculumCourseForm)


class AcademicYearAdmin(admin.ModelAdmin):
    actions = ['activate']
    list_display = [
        'code', 'school_year', 'semester', 'date_start', 'date_registration', 'date_preparation',
        'date_completion', 'date_end', 'is_active'
    ]

    def activate(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Please select only 1 %s " % self.opts.verbose_name)
        else:
            for item in queryset:
                item.activate()
                self.message_user(request, "%s activated" % item)

    activate.short_description = _('Activate selected academic year')


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


class CurriculumAdmin(ModelAdmin):
    inspect_enabled = True
    inspect_template = 'admin/curriculum_inspect.html'
    form = CurriculumForm
    search_fields = ['name', 'rmu__name']
    actions = ['activate']
    list_filter = ['is_active', ProgramStudyFilter]
    list_select_related = ['rmu']
    list_display = ['name', 'rmu', 'year', 'sks_graduate', 'is_active']
    raw_id_fields = ['rmu']
    fieldsets = (
        (None, {
            'fields': ('code', 'name', 'rmu', 'year', 'sks_graduate', 'is_public')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('summary', 'description'),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return Curriculum.objects.get_with_summary(qs)

    def activate(self, request, queryset):
        for item in queryset:
            item.activate()
        self.message_user(request, "%s %s activated" % (queryset.count(), self.opts.verbose_name))

    activate.short_description = _('Activate selected curriculums')

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


class CourseAdmin(ImportExportMixin, ExportActionMixin, ModelAdmin):
    form = CourseForm
    formats = (base_formats.XLSX,)
    resource_class = CourseResource
    inspect_enabled = True
    inspect_template = 'admin/course_inspect.html'
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


class TeacherInline(admin.TabularInline):
    min_num = 1
    model = Teacher
    list_select_related = ['rmu']
    raw_id_fields = ['rmu']


class TeacherAdmin(ImportExportMixin, ExportActionMixin, ModelAdmin):
    formats = (base_formats.XLSX,)
    resource_class = TeacherResource
    inspect_enabled = True
    inspect_template = 'admin/teacher_inspect.html'
    list_display = ['name', 'tid', 'rmu', 'is_active']
    raw_id_fields = ['account']
    search_fields = ['account__first_name', 'tid']
    list_select_related = ['rmu', 'account']
    list_filter = ['rmu']


class StudentAdmin(ImportExportMixin, ExportActionMixin, ModelAdmin):
    formats = (base_formats.XLSX,)
    resource_class = StudentResource
    inspect_enabled = True
    inspect_template = 'admin/student_inspect.html'
    search_fields = ['account__first_name', 'student_id']
    list_select_related = ['account', 'rmu', 'year_of_force', 'coach', 'curriculum']
    list_filter = ['status', 'year_of_force', 'registration']
    list_display = ['account', 'student_id', 'rmu', 'year_of_force', 'registration', 'status']
    fields = ['account', 'student_id', 'coach', 'rmu', 'curriculum', 'year_of_force', 'semester',
              'registration', 'registration_id', 'status', 'status_note', 'primary']
    raw_id_fields = ['account', 'rmu', 'year_of_force', 'curriculum', 'coach']


class ScoreRangeAdmin(admin.ModelAdmin):
    list_display = ['schema', 'alphabetic', 'numeric', 'min_point', 'max_point', 'predicate']


class PlainStudentScoreAdmin(admin.ModelAdmin):
    search_fields = []
    raw_id_fields = ['student', 'course']
    list_display = ['student', 'course', 'alphabetic', 'numeric']


class ConversionStudentScoreAdmin(admin.ModelAdmin):
    search_fields = [
        'course__course__name', 'course__course__inner_id',
        'student__account__first_name', 'student__student_id'
    ]
    raw_id_fields = ['student', 'course']
    list_display = ['student', 'course', 'sks', 'alphabetic', 'numeric', 'point',
                    'ori_code', 'ori_name', 'ori_numeric', 'ori_alphabetic']


class StudentConversionItemAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = StudentConversionItemResource
    list_display = ['conversion', 'course']


class StudentConversionItemInline(admin.StackedInline):
    extra = 0
    min_num = 1
    model = StudentConversionItem
    raw_id_fields = ['course']


class StudentConversionAdmin(ModelAdmin):
    inspect_enabled = True
    inspect_template = 'admin/conversion_inspect.html'
    list_display = ['inner_id', 'student', 'ori_institution_name', 'created_at', 'status', 'is_trash']
    list_select_related = ['student']
    search_fields = ['student__account__name']
    inlines = [StudentConversionItemInline]
    raw_id_fields = ['student']
    actions = ['mark_as_draft', 'mark_as_valid', 'mark_as_posted', 'mark_as_canceled', 'trash', 'restore']

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.is_editable and super().has_change_permission(request, obj)

    def trash(self, request, queryset):
        for item in queryset:
            item.delete(paranoid=True, user=request.user)
        if queryset.count() == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully marked as trash." % message_bit)

    trash.short_description = _('Move selected Student Conversion to trash')

    def restore(self, request, queryset):
        for item in queryset:
            item.restore()
        if queryset.count() == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully restored." % message_bit)

    restore.short_description = _('Restore selected Student Conversion')

    def mark_as_draft(self, request, queryset):
        for item in queryset:
            item.mark_as_draft()
        if queryset.count() == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully marked as draft." % message_bit)

    mark_as_draft.short_description = _('Draft selected Student Conversion')

    def mark_as_valid(self, request, queryset):
        for item in queryset:
            item.mark_as_valid()
        if queryset.count() == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully marked as valid." % message_bit)

    mark_as_valid.short_description = _('Validate selected Student Conversion')

    def mark_as_canceled(self, request, queryset):
        for item in queryset:
            item.mark_as_canceled()
        if queryset == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully canceled." % message_bit)

    mark_as_canceled.short_description = _('Cancel selected Student Conversion')

    def mark_as_posted(self, request, queryset):
        for item in queryset:
            item.mark_as_posted()
        if queryset == 1:
            message_bit = "1 student conversion was"
        else:
            message_bit = "%s student conversions were" % queryset.count()
        self.message_user(request, "%s successfully posted." % message_bit)

    mark_as_posted.short_description = _('Post selected Student Conversion')
