from django.urls import path
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, Http404, reverse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_websites.views import EditView, DeleteView, CreateView
from django_websites.options import ModelSite, ModelSiteGroup
from django_websites import messages

from ...academic.models import Student
from .student_views import StudentHomeView, StudentScoresView, StudentSetAsPrimary



class StudentSiteGroup(ModelSiteGroup):
    namespace = 'student'
    items = []

    def get_urls(self):
        urlpatterns = [
            path('student/manage/', StudentHomeView.as_view(), name='account_student_manage'),
            path('student/scores/', StudentScoresView.as_view(), name='account_student_scores'),
            path('student/set_primary/', StudentSetAsPrimary.as_view(), name='account_student_set_primary'),
        ]
        urls = super().get_urls()
        return urlpatterns + urls


student_site = StudentSiteGroup()
