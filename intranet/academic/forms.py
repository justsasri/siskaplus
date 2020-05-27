from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple
from django_trumbo.widgets import TrumbowygWidget

from .models import Concentration, Course, Curriculum, CurriculumCourse


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    summary = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 30em'}))
    description = forms.CharField(
        required=False,
        widget=TrumbowygWidget()
    )


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = '__all__'

    summary = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'style': 'width: 30em'}))
    description = forms.CharField(
        required=False,
        widget=TrumbowygWidget()
    )


class CurriculumCourseForm(forms.ModelForm):
    class Meta:
        model = CurriculumCourse
        fields = '__all__'

    concentration = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Concentration.objects.all(),
        widget=FilteredSelectMultiple(
            verbose_name=_('Concentration'),
            is_stacked=False
        )
    )
