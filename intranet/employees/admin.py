from django.contrib import admin
from django.utils import translation, timezone
from mptt.admin import MPTTModelAdmin

from .models import Department, Position, Employee, Employment, ExtraPosition

_ = translation.gettext_lazy


@admin.register(Department)
class DepartmentAdmin(MPTTModelAdmin):
    show_in_index = True
    search_fields = ['name']
    list_display = ['name', 'code', 'level']


@admin.register(Position)
class PositionAdmin(MPTTModelAdmin):
    show_in_index = True
    search_fields = ['department__name']
    list_select_related = ['department']
    list_display = ['name', 'level', 'department', 'is_manager', 'is_co_manager']


@admin.register(ExtraPosition)
class ChairmanAdmin(admin.ModelAdmin):
    list_display = ['is_active']
    list_select_related = ['employee', 'position']

    def department(self, obj):
        return obj.position.department


class EmployeeInline(admin.TabularInline):
    min_num = 1
    model = Employee
    exclude = ['creator', 'date_created']


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    show_in_index = True
    search_fields = ['eid', ]
    list_display = ['eid', 'account', 'is_active_label']
    list_select_related = ['account', 'department']

    def is_active_label(self, obj):
        return obj.is_active

    is_active_label.boolean = True
    is_active_label.short_description = _("active")


@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    pass
