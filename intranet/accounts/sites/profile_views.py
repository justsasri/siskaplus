from django.views.generic.edit import UpdateView
from django.shortcuts import reverse
from django_websites.views import InspectView, EditView

from ...persons.models import Contact, SocialMedia

class ProfileUpdateView(EditView):
    """ Account Profile Update View
        permissions: is_login, is_owner
    """

    template_name = 'profile/update.html'

    def get_success_message_buttons(self, instance):
        return []

    def check_action_permitted(self, user):
        return True

    def get_context_data(self, **kwargs):
        is_mine = self.instance.account == self.request.user
        context = {
            'is_mine': is_mine
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class ProfilePublicView(InspectView):
    template_name = 'profile/public.html'

    def check_action_permitted(self, user):
        return True

    def get_context_data(self, **kwargs):
        is_mine = self.instance.account == self.request.user
        context = {
            'is_mine': is_mine,
            'person': self.request.user.person
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class ProfileContactUpdateView(UpdateView):
    model = Contact
    fields = ['phone', 'whatsapp', 'fax', 'website']
    template_name = 'profile/edit.html'

    def get_success_url(self):
        return reverse('account_home')

    def get_context_data(self, **kwargs):
        context = {
            'view': self,
            'opts': self.model._meta,
            'page_title': 'Updating contacts',
            'page_subtitle': '%s contacts' % str(self.request.user),
            'meta_title': 'Updating %s contacts' % str(self.request.user),
        }
        context.update(**kwargs)
        return super().get_context_data(**context)


class ProfileSocialMediaUpdateView(UpdateView):
    model = SocialMedia
    fields = ['instagram', 'facebook', 'twitter', 'youtube']
    template_name = 'profile/edit.html'

    def get_fields(self):
        return self.fields or [field.name for field in self.model._meta.get_fields()]

    def get_success_url(self):
        return reverse('account_home')

    def get_context_data(self, **kwargs):
        context = {
            'view': self,
            'opts': self.model._meta,
            'page_title': 'Updating social media',
            'page_subtitle': '%s social media accounts' % str(self.request.user),
            'meta_title': 'Updating %s social media accounts' % str(self.request.user),
        }
        context.update(**kwargs)
        return super().get_context_data(**context)