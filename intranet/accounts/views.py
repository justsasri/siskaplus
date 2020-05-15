from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

@method_decorator([login_required], name='dispatch')
class AccountHomeView(TemplateView):
    template_name = 'account/home.html'

    def get_context_data(self, **kwargs):
        person = getattr(self.request.user, 'person', None)
        context = {
            'instance': self.request.user,
            'person': person,
            'page_title': person if person else self.request.user,
            'page_subtitle': '@%s' % self.request.user.username,
            'is_mine': True
        }
        context.update(**kwargs)
        return super().get_context_data(**context)
