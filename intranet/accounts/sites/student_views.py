from django.views import View
from django.views.generic import TemplateView
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django_websites import messages

from ...academic.models import Student
from ..decorators import student_required


class StudentHomeView(TemplateView):
    template_name = 'account/student.html'

    @method_decorator([login_required, student_required])
    def dispatch(self, request, *args, **kwargs):
        return super(StudentHomeView, self).dispatch(request, *args, **kwargs)


class StudentScoresView(TemplateView):
    template_name = 'account/student_scores.html'


class StudentSetAsPrimary(View):
    @method_decorator(login_required)
    def post(self, request):
        instance_pk = request.POST.get('student')
        student = get_object_or_404(Student, pk=instance_pk)
        try:
            student.set_as_primary()
            msg = _("Student %s is set as your primary student") % student.student_id
            messages.success(request, msg.title())
            return redirect(reverse('account_student_manage'))
        except Exception as err:
            messages.error(request, err)
            return redirect(reverse('account_student_manage'))
