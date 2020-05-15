from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from allauth.account import app_settings
from allauth.utils import get_form_class
from allauth.exceptions import ImmediateHttpResponse
from allauth.account import signals
from allauth.account.views import SignupView as SignupViewBase
from allauth.account.utils import perform_login, get_adapter

from .forms import MatriculantSignupForm


class MatriculantAppIndex(TemplateView):
    template_name = 'sites/matriculants/app_index.html'


def complete_matriculant_signup(request, user, email_verification, success_url, signal_kwargs=None):
    signal_kwargs = {} if signal_kwargs is None else signal_kwargs
    signals.user_signed_up.send(sender=user.__class__, request=request, user=user, **signal_kwargs)
    return perform_login(
        request, user, email_verification,
        signup=True, redirect_url=success_url, signal_kwargs=signal_kwargs
    )


class MatriculantSignupView(SignupViewBase):
    template_name = "sites/matriculants/accounts/signup.html"
    form_class = MatriculantSignupForm
    template_name_signup_closed = ''
    redirect_field_name = "next"
    success_url = None

    def is_open(self):
        return get_adapter(self.request).is_matriculant_open_for_signup(self.request)

    def closed(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_signup_closed,
        }
        return self.response_class(**response_kwargs)

    def get_form_class(self):
        return get_form_class(app_settings.FORMS, 'student_signup', self.form_class)

    def form_valid(self, form):
        # By assigning the User to a property on the view, we allow subclasses
        # of SignupView to access the newly created User instance
        self.user = form.save(self.request)
        try:
            return complete_matriculant_signup(
                self.request, self.user,
                app_settings.EMAIL_VERIFICATION,
                self.get_success_url())
        except ImmediateHttpResponse as e:
            return e.response

    def get_context_data(self, **kwargs):
        ret = super().get_context_data(**kwargs)
        return ret
