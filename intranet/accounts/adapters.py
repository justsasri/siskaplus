from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Disable registration/signup
    """

    def is_open_for_signup(self, request):
        return False

    def is_matriculant_open_for_signup(self, request):
        return True


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Disable registration/signup
    """

    def is_open_for_signup(self, request):
        return False