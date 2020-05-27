from django.urls import path
from django.shortcuts import render, reverse, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django_websites.options import ModelSite, ModelSiteGroup
from django_websites.views import InspectView

from ..lectures.models import Lecture
from ..lectures.enums import LectureStatus
from ..lectures.filters import LectureFilter
from .models import (
    Curriculum,
    Course,
    Teacher,
    Student
)

from .filters import CourseFilter, CurriculumFilter, TeacherFilter, StudentFilter


class AcademicIndexView(TemplateView):
    template_name = 'sites/academic/app_index.html'

    @method_decorator(login_required)
    @method_decorator(permission_required('global_permission.access_academic_apps', raise_exception=True))
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super(AcademicIndexView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs = super(AcademicIndexView, self).get_context_data(**kwargs)
        top_teachers = Teacher.objects.get_top_teachers()[:12]
        kwargs.update({
            'top_teachers': top_teachers,
            'courses': Course.objects.all()[:6],
            'courses_count': Course.objects.filter(is_active=True).count(),
            'curriculums': Curriculum.objects.all()[:6],
            'curriculums_count': Curriculum.objects.filter(is_active=True).count(),
        })
        return kwargs


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix='curriculum')], name='index_view')
@method_decorator([cache_page(settings.CACHE_TTL, key_prefix='curriculum')], name='inspect_view')
class CurriculumModelSite(ModelSite):
    model = Curriculum
    filterset_class = CurriculumFilter
    inspect_view_enabled = True
    select_related = ['rmu']


@method_decorator([cache_page(settings.CACHE_TTL, key_prefix='course')], name='index_view')
@method_decorator([cache_page(settings.CACHE_TTL, key_prefix='course')], name='inspect_view')
class CourseModelSite(ModelSite):
    model = Course
    filterset_class = CourseFilter
    inspect_view_enabled = True
    select_related = ['rmu', 'course_type', 'course_group']


class TeacherInspectCoursesView(InspectView):
    template_name = 'sites/academic/teacher/inspect_courses.html'


class TeacherModelSite(ModelSite):
    model = Teacher
    filterset_class = TeacherFilter
    inspect_view_enabled = True
    inspect_courses_view_class = TeacherInspectCoursesView
    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('teacher/inspect/<str:instance_pk>/courses/', self.inspect_courses_view, name='academic_teacher_courses'),
        ]
        return urls

    def inspect_courses_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_courses_view_class
        return view_class.as_view(**kwargs)(request)


class StudentModelSite(ModelSite):
    model = Student
    filterset_class = StudentFilter
    inspect_view_enabled = True

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('student/profile/<str:instance_pk>/', self.profile_view, name='person_profile'),
        ]
        return urls

    def profile_view(self, request, instance_pk):
        instance = get_object_or_404(Student, pk=instance_pk)
        is_mine = instance.person.account == request.user
        context = {
            'page_subtitle': 'Student profile',
            'instance': instance.person,
            'is_mine': is_mine
        }
        return render(request, 'sites/profile/public.html', context=context)


class AcademicSiteGroup(ModelSiteGroup):
    namespace = 'academic'
    items = [
        CourseModelSite,
        CurriculumModelSite,
        TeacherModelSite,
        StudentModelSite
    ]

    def get_urls(self):
        urlpatterns = [
            path('', AcademicIndexView.as_view(), name='academic_app_index'),
        ]
        urls = super().get_urls()
        return urlpatterns + urls


academic_site = AcademicSiteGroup()
