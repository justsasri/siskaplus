from django.urls import path
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, reverse, redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages import constants

from django_websites.options import ModelSite, ModelSiteGroup
from django_websites.views import IndexView
from django_websites.messages import messages

from ..accounts.decorators import student_required
from ..academic.enums import StudentStatus
from .enums import EnrollmentCriteria, LectureStatus
from .models import Lecture, StudentPlan
from .filters import LectureFilter


class ClassroomIndexView(TemplateView):
    template_name = 'sites/classrooms/app_index.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs.update({
            'lectures': Lecture.objects.filter(status='PUB')[:6],
            'lectures_count': Lecture.objects.filter(status='PUB').count(),
        })
        return kwargs


class LectureModelSite(ModelSite):
    model = Lecture
    index_view_enabled = True
    inspect_view_enabled = True
    filterset_class = LectureFilter
    select_related = ['curriculum_course', 'teacher', 'room']

    def get_queryset(self, request):
        qs = super(LectureModelSite, self).get_queryset(request)
        return qs.filter(status=LectureStatus.PUBLISHED.value)


class StudentPlanIndexView(IndexView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.primary_student:
            # handle validation with message
            msg = _("%s, Are you a student? please select your primary student.")
            messages.add_message(request, constants.ERROR, message=msg % request.user)
            return redirect(reverse('classrooms_lecture_index'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        lectures = StudentPlan.objects.filter(student=self.request.user.primary_student)
        kwargs.update({
            'lectures': lectures,
        })
        return kwargs


class StudentPlanModelSite(ModelSite):
    model = StudentPlan
    index_view_enabled = True
    index_view_class = StudentPlanIndexView
    inspect_view_enabled = False
    create_view_enabled = False
    edit_view_enabled = False
    delete_view_enabled = False
    filterset_fields = ['id']

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('studentplan/add/<str:instance_pk>/',
                 self.add_to_plan_view,
                 name='classrooms_studentplan_add'),
            path('studentplan/remove/<str:instance_pk>/',
                 self.remove_from_plan_view,
                 name='classrooms_studentplan_remove'),
            path('studentplan/clean/',
                 self.clean_plan_view,
                 name='classrooms_studentplan_clean'),
        ]
        return urls

    def add_to_plan_view(self, request, instance_pk):
        """ Add selected lecture to current user student plan """
        lecture = get_object_or_404(Lecture, pk=instance_pk)
        try:
            lecture.add_to_plan(request)
            return redirect(reverse('classrooms_studentplan_index'))
        except ValidationError as err:
            # handle validation with message
            messages.add_message(request, constants.ERROR, message="<br/>".join(err))
            return redirect(reverse('classrooms_studentplan_index'))

    def remove_from_plan_view(self, request, instance_pk):
        """ remove selected lecture from current user student plan """
        plan_item = get_object_or_404(
            StudentPlan,
            pk=instance_pk,
            student=request.user.primary_student
        )
        msg = _('"%s" deleted successfully.') % plan_item.lecture
        plan_item.delete()
        messages.add_message(request, constants.SUCCESS, message=msg)
        return redirect(reverse('classrooms_studentplan_index'))

    def clean_plan_view(self, request):
        """ remove all lecture from current user student plan """
        plan_item = self.model.objects.filter(student=request.user.primary_student)
        plan_item.delete()
        msg = _('Your plan cleaned successfully.')
        messages.add_message(request, constants.SUCCESS, message=msg)
        return redirect(reverse('classrooms_studentplan_index'))


class ClassroomModelSiteGroup(ModelSiteGroup):
    namespace = 'classrooms'
    items = [LectureModelSite, StudentPlanModelSite]

    def get_urls(self):
        urlpatterns = [
            path('', ClassroomIndexView.as_view(), name='classrooms_app_index'),
        ]
        urls = super().get_urls()
        return urlpatterns + urls


classroom_sites = ClassroomModelSiteGroup()
