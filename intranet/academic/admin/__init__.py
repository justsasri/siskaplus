from django.contrib import admin
from django.contrib.auth import get_user_model
from ...admin.sites import admin_site
from .sites import academic_admin
from .admin import *

admin.site.register(SchoolYear, admin.ModelAdmin)
admin.site.register(AcademicYear, AcademicYearAdmin)
admin.site.register(ManagementUnit, ManagementUnitAdmin)
admin.site.register(Concentration, admin.ModelAdmin)
admin.site.register(CourseType, admin.ModelAdmin)
admin.site.register(CourseGroup, admin.ModelAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Curriculum, CurriculumAdmin)
admin.site.register(CurriculumCourse, CurriculumCourseAdmin)

admin.site.register(ScoreRange, ScoreRangeAdmin)
admin.site.register(PlainStudentScore, PlainStudentScoreAdmin)
admin.site.register(ConversionStudentScore, ConversionStudentScoreAdmin)
admin.site.register(StudentConversion, StudentConversionAdmin)
admin.site.register(StudentConversionItem, StudentConversionItemAdmin)

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)

# academic admins

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
academic_admin.register(PlainStudentScore, PlainStudentScoreAdmin)
academic_admin.register(ConversionStudentScore, ConversionStudentScoreAdmin)
academic_admin.register(StudentConversion, StudentConversionAdmin)
