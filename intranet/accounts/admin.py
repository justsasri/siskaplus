from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as UserAdminBase

from import_export.admin import ImportExportMixin, ExportActionMixin
from import_export.formats import base_formats

from ..admin.sites import admin_site
from .models import User
from .resources import UserResource


class UserAdmin(ImportExportMixin, ExportActionMixin, UserAdminBase):
    resource_class = UserResource
    formats = (base_formats.XLSX,)
    list_display = [
        'username', 'email', 'is_staff', 'is_active', 'is_superuser',
        'is_student', 'is_teacher', 'is_management', 'is_employee', 'is_applicant', 'is_matriculant',
    ]
    fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'password')}),
        (_('Title'), {'fields': ('title', 'front_title', 'back_title', 'show_title', 'show_academic_title')}),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_staff',
                       'is_student',
                       'is_teacher',
                       'is_management',
                       'is_employee',
                       'is_applicant',
                       'is_matriculant',
                       'is_superuser',
                       'groups',
                       'user_permissions'
                       ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    non_superuser_fieldsets = (
        (None, {'fields': ('username', 'email', 'first_name', 'password')}),
        (_('Title'), {'fields': ('title', 'front_title', 'back_title', 'show_title', 'show_academic_title')}),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_student',
                       'is_teacher',
                       'is_management',
                       'is_employee',
                       'is_applicant',
                       'is_matriculant',
                       'groups',
                       'user_permissions'
                       ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (_('User Account'), {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        (_('Personal Info'), {
            'classes': ('wide',),
            'fields': ('title', 'front_title', 'first_name', 'back_title', 'show_title',
                       'show_academic_title'),
        }),
        (_('Permissions'), {
            'fields': ('is_active',
                       'is_student',
                       'is_teacher',
                       'is_management',
                       'is_employee',
                       'is_applicant',
                       'is_matriculant',
                       ),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if not request.user.is_superuser:
            return self.non_superuser_fieldsets
        return super().get_fieldsets(request, obj)


admin_site.register(User, UserAdmin)