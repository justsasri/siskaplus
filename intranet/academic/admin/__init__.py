from django.contrib.auth import get_user_model
from ...accounts.admin import UserAdmin
from ...admin.sites import admin_site
from .sites import academic_admin
from .admin import *

admin_site.register(SchoolYear, admin.ModelAdmin)
admin_site.register(AcademicYear, AcademicYearAdmin)
admin_site.register(ManagementUnit, ManagementUnitAdmin)
admin_site.register(Concentration, admin.ModelAdmin)
admin_site.register(CourseType, admin.ModelAdmin)
admin_site.register(CourseGroup, admin.ModelAdmin)
admin_site.register(Course, CourseAdmin)
admin_site.register(Curriculum, CurriculumAdmin)
admin_site.register(CurriculumCourse, CurriculumCourseAdmin)

admin_site.register(ScoreRange, ScoreRangeAdmin)
admin_site.register(PlainStudentScore, PlainStudentScoreAdmin)
admin_site.register(ConversionStudentScore, ConversionStudentScoreAdmin)
admin_site.register(StudentConversion, StudentConversionAdmin)
admin_site.register(StudentConversionItem, StudentConversionItemAdmin)

admin_site.register(Student, StudentAdmin)
admin_site.register(Teacher, TeacherAdmin)

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
academic_admin.register(get_user_model(), UserAdmin)
academic_admin.register(StudentConversion, StudentConversionAdmin)
