from django.contrib import admin

from ...lectures.models import (
    Lecture, LectureStudent, LectureScoreWeighting,
    LectureSchedule, StudentPlan, Enrollment, EnrollmentItem,
    StudentAttendance, TeacherAttendance
)


class LectureScoreWeightInline(admin.TabularInline):
    extra = 0
    model = LectureScoreWeighting
    exclude = ['created_by', 'modified_by', 'date_created', 'date_modified']


class LectureSceduleInline(admin.TabularInline):
    extra = 0
    model = LectureSchedule
    raw_id_fields = ['room']
    ordering = ('date',)

    def get_max_num(self, request, obj=None, **kwargs):
        """ Set max num based on order_item.order_qty """
        try:
            kwarg = request.resolver_match.kwargs
            parent_id = kwarg.get('object_id')
            parent = Lecture.objects.get(pk=parent_id)
            return parent.series
        except Exception:
            return super().get_max_num(request, obj=obj)


class LectureStudentInline(admin.TabularInline):
    extra = 0
    model = LectureStudent
    raw_id_fields = ['student']


class StudentAttendanceInline(admin.TabularInline):
    extra = 0
    model = StudentAttendance


class TeacherAttendanceInline(admin.TabularInline):
    extra = 0
    max_num = 2
    model = TeacherAttendance


@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    search_fields = ['teacher__person__fullname', 'curriculum_course__course__name']
    inlines = [LectureSceduleInline]
    list_display = ['curriculum_course', 'teacher', 'room', 'time_start', 'date_start', 'series', 'duration']
    raw_id_fields = ['teacher', 'assistant', 'curriculum_course', 'academic_year', 'room']
    fields = [
        'teacher', 'assistant', 'curriculum_course', 'academic_year', 'min_capacity', 'max_capacity', 'room',
        'duration', 'series',
        'time_start',
        'date_start', 'status']


@admin.register(LectureStudent)
class LectureStudentAdmin(admin.ModelAdmin):
    list_display = ['student', 'lecture', 'status']
    search_fields = ['student__person__fullname', 'lecture__name']
    raw_id_fields = ['student', 'lecture']


@admin.register(LectureScoreWeighting)
class LectureScoreWeigtingAdmin(admin.ModelAdmin):
    list_select_related = ['lecture']
    raw_id_fields = ['lecture']
    list_display = [
        'lecture', 'attendance', 'homework1', 'homework2', 'quis1', 'quis2',
        'mid_exam', 'final_exam', 'total']


@admin.register(LectureSchedule)
class LectureSceduleAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    search_fields = [
        'lecture__name', 'lecture__inner_id', 'room__name',
        'lecture__teacher__person__fullname']
    inlines = [TeacherAttendanceInline, StudentAttendanceInline]
    list_display = ['lecture', 'session', 'room', 'date', 'time_start', 'time_end', 'type']
    raw_id_fields = ['lecture', 'room']
    radio_fields = {
        "type": admin.HORIZONTAL,
    }


class EnrollmentItemLine(admin.TabularInline):
    extra = 0
    model = EnrollmentItem
    raw_id_fields = ['lecture']


@admin.register(StudentPlan)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    raw_id_fields = ['student']
    list_display = ['inner_id', 'student', 'created_at']
    search_fields = ['student__sid', 'student__person__fullname']
    inlines = [EnrollmentItemLine]


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'schedule', 'note']


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'schedule', 'status', 'note']
