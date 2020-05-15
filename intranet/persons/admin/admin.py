from django.contrib import admin
from ..resources import PersonResource
from ..models import (
    Person,
    Contact,
    SocialMedia,
    PersonAddress,
    FormalEducation,
    NonFormalEducation,
    Working,
    Volunteer,
    Skill,
    Publication,
    Family,
    Award
)


class EducationLevelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ['slug', 'name', 'description']


class ContactInline(admin.StackedInline):
    extra = 0
    model = Contact


class SocialMediaInline(admin.StackedInline):
    extra = 0
    model = SocialMedia


class PersonAddressInline(admin.StackedInline):
    extra = 0
    max_num = 2
    model = PersonAddress


class FormalEducationInline(admin.StackedInline):
    extra = 0
    model = FormalEducation


class NonFormalEducationInline(admin.StackedInline):
    extra = 0
    model = NonFormalEducation


class WorkingInline(admin.StackedInline):
    extra = 0
    model = Working


class OrganizationInline(admin.StackedInline):
    extra = 0
    model = Volunteer


class SkillsInline(admin.TabularInline):
    extra = 0
    model = Skill


class AwardsInline(admin.StackedInline):
    extra = 0
    model = Award


class PublicationsInline(admin.StackedInline):
    extra = 0
    model = Publication


class FamilyInline(admin.StackedInline):
    extra = 0
    model = Family


class PersonAdmin(admin.ModelAdmin):
    resource_class = PersonResource
    list_select_related = ['account']
    list_display = ['pid', 'account', 'date_of_birth']
    raw_id_fields = ['account']
    inlines = [
        ContactInline,
        SocialMediaInline,
        PersonAddressInline,
        FormalEducationInline,
        NonFormalEducationInline,
        SkillsInline,
        AwardsInline,
        WorkingInline,
        OrganizationInline,
        PublicationsInline,
        FamilyInline
    ]
    fieldsets = (
        (None, {
            'fields': (
                'account', 'pid', 'nickname', 'gender', 'date_of_birth', 'religion', 'nation', 'about_me')
        }),
    )


class FormalEducationAdmin(admin.ModelAdmin):
    list_display = ['person', 'level']


class NonFormalEducationAdmin(admin.ModelAdmin):
    list_display = ['person']


class WorkingAdmin(admin.ModelAdmin):
    list_display = ['person', 'institution']


class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['person', 'organization']


class SkillsAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


class AwardsAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


class PublicationAadmin(admin.ModelAdmin):
    list_display = ['person', 'title']


class FamilyAdmin(admin.ModelAdmin):
    list_display = ['person', 'name']


admin.site.register(Person, PersonAdmin)
admin.site.register(FormalEducation, FormalEducationAdmin)
admin.site.register(NonFormalEducation, NonFormalEducationAdmin)
admin.site.register(Working, WorkingAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
admin.site.register(Skill, SkillsAdmin)
admin.site.register(Award, AwardsAdmin)
admin.site.register(Publication, PublicationAadmin)
admin.site.register(Family, FamilyAdmin)
