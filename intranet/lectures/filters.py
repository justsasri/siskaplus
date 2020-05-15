from django import forms
from django.utils.translation import ugettext_lazy as _

import django_filters as filters

from ..academic.enums import ManagementLevel, Semester
from ..academic.models import Curriculum, ManagementUnit, AcademicYear
from .models import Lecture


class LectureFilter(filters.FilterSet):
    class Meta:
        model = Lecture
        fields = {
            'course__name': ['icontains']
        }

    course_name = filters.CharFilter(
        field_name='course__name',
        label=_('name'), lookup_expr='icontains')
    academic_year = filters.ModelMultipleChoiceFilter(
        label=_('academic year'),
        queryset=AcademicYear.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    semester = filters.MultipleChoiceFilter(
        label=_('Semester'),
        field_name='curriculum_course__semester_number',
        choices=[(x, str(x)) for x in range(1, 9)],
        widget=forms.CheckboxSelectMultiple)
    curriculum__rmu = filters.ModelMultipleChoiceFilter(
        label=_('program study'),
        queryset=ManagementUnit.objects.filter(
            type=ManagementLevel.PROGRAM_STUDY.value
        ).only('id', 'name').order_by('level'),
        widget=forms.CheckboxSelectMultiple)
