from allauth import app_settings
from allauth.account.forms import SignupForm

auth_settings = app_settings.settings


class MatriculantSignupForm(SignupForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
