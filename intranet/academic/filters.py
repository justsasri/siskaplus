from django import forms
from django.utils.translation import ugettext_lazy as _

import django_filters as filters

from ..academic.enums import StudentStatus
from .models import (
    SchoolYear,
    ManagementLevel,
    ManagementUnit,
    Curriculum,
    Course,
    CourseGroup,
    CourseType,
    Teacher,
    Student,
)


class CourseFilter(filters.FilterSet):
    class Meta:
        model = Course
        fields = {
            'name': ['icontains']
        }

    course_name = filters.CharFilter(
        field_name='name', label=_('name'), lookup_expr='icontains')
    rmu = filters.ModelMultipleChoiceFilter(
        queryset=ManagementUnit.objects.only('id', 'name').order_by('level'),
        widget=forms.CheckboxSelectMultiple)
    curriculum_courses__curriculum = filters.ModelMultipleChoiceFilter(
        label='curriculum',
        queryset=Curriculum.objects.only('id', 'name'),
        widget=forms.CheckboxSelectMultiple)
    course_type = filters.ModelMultipleChoiceFilter(
        queryset=CourseType.objects.only('id', 'name'),
        widget=forms.CheckboxSelectMultiple)
    course_group = filters.ModelMultipleChoiceFilter(
        queryset=CourseGroup.objects.only('id', 'name'),
        widget=forms.CheckboxSelectMultiple)


class CurriculumFilter(filters.FilterSet):
    class Meta:
        model = Curriculum
        fields = {
            'name': ['icontains']
        }

    curriculum_name = filters.CharFilter(
        field_name='name', label=_('name'), lookup_expr='icontains')
    rmu = filters.ModelMultipleChoiceFilter(
        queryset=ManagementUnit.objects.filter(type=ManagementLevel.PROGRAM_STUDY.value),
        widget=forms.CheckboxSelectMultiple)


class TeacherFilter(filters.FilterSet):
    class Meta:
        model = Teacher
        fields = ['account__first_name']

    fullname = filters.CharFilter(
        field_name='account__first_name', label=_('name'), lookup_expr='icontains')
    rmu = filters.ModelMultipleChoiceFilter(
        queryset=ManagementUnit.objects.filter(type=ManagementLevel.PROGRAM_STUDY.value),
        widget=forms.CheckboxSelectMultiple)


class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['account__first_name']

    fullname = filters.CharFilter(
        field_name='account__first_name', label=_('Name'), lookup_expr='icontains')
    rmu = filters.ModelMultipleChoiceFilter(
        queryset=ManagementUnit.objects.filter(type=ManagementLevel.PROGRAM_STUDY.value),
        widget=forms.CheckboxSelectMultiple)
    status = filters.MultipleChoiceFilter(
        field_name='status', choices=StudentStatus.CHOICES.value,
        label='status', widget=forms.CheckboxSelectMultiple)
    year_of_force = filters.ModelMultipleChoiceFilter(
        queryset=SchoolYear.objects.all(),
        widget=forms.CheckboxSelectMultiple)
