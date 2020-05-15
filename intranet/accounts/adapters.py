from allauth.account.adapter import DefaultAccountAdapter


class NoSignupAdapter(DefaultAccountAdapter):
    """
    Disable registration/signup
    """

    def is_open_for_signup(self, request):
        return False

    def is_matriculant_open_for_signup(self, request):
        return True
