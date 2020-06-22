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
from .enums import StudentStatus
from .models import Curriculum, Course, Teacher, Student

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


class TeacherInspectStudentsView(InspectView):
    template_name = 'sites/academic/teacher/inspect_students.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        # filter teacher's students by query args status
        status = self.request.GET.get('status', None)
        if status:
            student_list = self.instance.students.filter(status=status)
        else:
            student_list = self.instance.students.all()
        kwargs.update({
            'students': student_list,
            'status_list': StudentStatus.CHOICES.value,
            'status_selected': status
        })
        return kwargs


class TeacherInspectLecturesView(InspectView):
    template_name = 'sites/academic/teacher/inspect_lectures.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        # filter teacher'slectures by query args status
        status = self.request.GET.get('status', None)
        if status:
            lecture_list = self.instance.lectures.filter(status=status)
        else:
            lecture_list = self.instance.lectures.all()
        kwargs.update({
            'lectures': lecture_list,
            'status_list': LectureStatus.CHOICES.value,
            'status_selected': status
        })
        return kwargs


class TeacherModelSite(ModelSite):
    model = Teacher
    filterset_class = TeacherFilter
    inspect_view_enabled = True
    inspect_courses_view_class = TeacherInspectCoursesView
    inspect_students_view_class = TeacherInspectStudentsView
    inspect_lectures_view_class = TeacherInspectLecturesView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('teacher/inspect/<str:instance_pk>/courses/', self.inspect_courses_view, name='academic_teacher_courses'),
            path('teacher/inspect/<str:instance_pk>/students/', self.inspect_students_view, name='academic_teacher_students'),
            path('teacher/inspect/<str:instance_pk>/lectures/', self.inspect_lectures_view, name='academic_teacher_lectures'),
        ]
        return urls

    def inspect_courses_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_courses_view_class
        return view_class.as_view(**kwargs)(request)

    def inspect_students_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_students_view_class
        return view_class.as_view(**kwargs)(request)

    def inspect_lectures_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_lectures_view_class
        return view_class.as_view(**kwargs)(request)


class StudentInspectCoursesView(InspectView):
    template_name = 'sites/academic/student/inspect_scores.html'


class StudentInspectLecturesView(InspectView):
    template_name = 'sites/academic/student/inspect_lectures.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        # filter student's lectures by query args status
        status = self.request.GET.get('status', None)
        if status:
            lecture_list = self.instance.lectures.filter(status=status)
        else:
            lecture_list = self.instance.lectures.all()
        kwargs.update({
            'lectures': lecture_list,
            'status_list': LectureStatus.CHOICES.value,
            'status_selected': status
        })
        return kwargs


class StudentModelSite(ModelSite):
    model = Student
    filterset_class = StudentFilter
    inspect_view_enabled = True
    inspect_scores_view_class = StudentInspectCoursesView
    inspect_lectures_view_class = StudentInspectLecturesView

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('student/profile/<str:instance_pk>/', self.profile_view, name='person_profile'),
            path('student/inspect/<str:instance_pk>/scores/', self.inspect_scores_view, name='academic_student_scores'),
            path('student/inspect/<str:instance_pk>/lectures/', self.inspect_lectures_view, name='academic_student_lectures'),
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

    def inspect_scores_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_scores_view_class
        return view_class.as_view(**kwargs)(request)

    def inspect_lectures_view(self, request, instance_pk):
        kwargs = {'modelsite': self, 'instance_pk': instance_pk}
        view_class = self.inspect_lectures_view_class
        return view_class.as_view(**kwargs)(request)


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
