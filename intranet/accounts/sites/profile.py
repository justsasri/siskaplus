from django.urls import path
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404, Http404, reverse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django_websites.views import EditView, DeleteView, CreateView
from django_websites.options import ModelSite, ModelSiteGroup
from django_websites import messages

from .profile_views import ProfilePublicView, ProfileUpdateView, ProfileContactUpdateView, ProfileSocialMediaUpdateView
from ...persons.models import (
    Person, Contact, SocialMedia, PersonAddress, FormalEducation,
    NonFormalEducation, Working, Volunteer, Award, Publication, Skill, Family
)


class PersonModelSite(ModelSite):
    model = Person
    index_view_enabled = False
    inspect_view_enabled = False
    create_view_enabled = False
    edit_view_enabled = False
    delete_view_enabled = False
    profile_update_view_class = ProfileUpdateView
    profile_public_view_class = ProfilePublicView
    profile_contact_update_class = ProfileContactUpdateView
    profile_socialmedia_update_class = ProfileSocialMediaUpdateView
    fields = [
        'pid', 'nickname', 'gender', 'religion', 'nation', 'date_of_birth', 'place_of_birth', 'about_me',
        'education_level', 'education_name', 'education_institution', 'year_graduate', 'privacy'
    ]

    def get_success_url(self):
        return reverse('account_manage')

    def get_urls(self):
        urls = super().get_urls()
        urls += [
            path('profile/', self.profile_update_view, name='account_manage'),
            path('contact/', self.profile_contact_update_view, name='account_contact_update'),
            path('socialmedia/', self.profile_socialmedia_update_view, name='account_socialmedia_update'),
            path('profile/<str:username>/', self.profile_public_view, name='public_profile'),
        ]
        return urls

    @method_decorator(login_required)
    def profile_update_view(self, request):
        if not hasattr(request.user, 'person'):
            raise Http404("You don't have person person object")
        kwargs = {'modelsite': self, 'instance_pk': str(request.user.person.id)}
        view_class = self.profile_update_view_class
        return view_class.as_view(**kwargs)(request)

    @method_decorator(login_required)
    def profile_contact_update_view(self, request):
        if not hasattr(request.user, 'person'):
            raise Http404("You don't have person person object")
        # create contact object if does not exist
        contact, created = Contact.objects.get_or_create(
            person=request.user.person,
            defaults={'person': request.user.person})
        pk = contact.id
        view_class = self.profile_contact_update_class
        return view_class.as_view()(request, pk=pk)

    @method_decorator(login_required)
    def profile_socialmedia_update_view(self, request):
        if not hasattr(request.user, 'person'):
            raise Http404("You don't have person person object")
        # create social media object if does not exist
        social_media, created = SocialMedia.objects.get_or_create(
            person=request.user.person,
            defaults={'person': request.user.person})
        pk = social_media.id
        view_class = self.profile_socialmedia_update_class
        return view_class.as_view()(request, pk=pk)

    def profile_public_view(self, request, username):
        user = get_object_or_404(get_user_model(), username=username)
        if not hasattr(user, 'person'):
            raise Http404("User doesn't have person object")
        kwargs = {'modelsite': self, 'instance_pk': str(user.person.id)}
        view_class = self.profile_public_view_class
        return view_class.as_view(**kwargs)(request)


class PersonHistoryCreateView(CreateView):

    def check_action_permitted(self, user):
        return True

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.person = self.request.user.person
        instance.save()
        messages.success(
            self.request, self.get_success_message(instance),
            buttons=self.get_success_message_buttons(instance)
        )
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('public_profile', args=(self.request.user.username,))


class PersonHistoryEditView(EditView):

    def check_action_permitted(self, user):
        return user.is_superuser or self.instance.person == user.person

    def get_success_url(self):
        return reverse('public_profile', args=(self.request.user.username,))


class PersonHistoryDeleteView(DeleteView):

    def check_action_permitted(self, user):
        return user.is_superuser or self.instance.person == user.person

    def get_success_url(self):
        return reverse('public_profile', args=(self.request.user.username,))


class PersonHistoryModelBase(ModelSite):
    index_view_enabled = False
    create_view_enabled = True
    edit_view_enabled = True
    delete_view_enabled = True
    create_view_class = PersonHistoryCreateView
    edit_view_class = PersonHistoryEditView
    delete_view_class = PersonHistoryDeleteView

    def get_template_names(self, action):
        return [
            '%s_%s_%s.html' % (self.namespace, self.opts.model_name, action),
            '%s_%s.html' % (self.namespace, action),
            # Deprecated respect to above naming format
            '%s/%s/%s.html' % (self.namespace, self.opts.model_name, action),
            '%s/%s.html' % (self.namespace, action),
            'sites/%s.html' % action,
        ]

class PersonAddressModelSite(PersonHistoryModelBase):
    model = PersonAddress
    fields = ['name', 'street', 'city', 'province', 'country', 'zipcode', 'privacy', 'is_primary']


class FormalEducationModelSite(PersonHistoryModelBase):
    model = FormalEducation
    fields = ['level', 'institution', 'major', 'date_start', 'date_end', 'status', 'document_link', 'privacy']


class NonFormalEducationModelSite(PersonHistoryModelBase):
    model = NonFormalEducation
    fields = ['name', 'description', 'institution', 'date_start', 'date_end', 'status', 'document_link', 'privacy']


class WorkingModelSite(PersonHistoryModelBase):
    model = Working
    fields = ['name', 'position', 'department', 'institution', 'description',
              'employment', 'date_start', 'date_end', 'document_link', 'privacy']


class VolunteerModelSite(PersonHistoryModelBase):
    model = Volunteer
    fields = ['organization', 'position', 'description', 'status',
              'date_start', 'date_end', 'document_link', 'privacy']


class AwardModelSite(PersonHistoryModelBase):
    model = Award
    fields = ['name', 'description', 'date', 'document_link', 'privacy']


class PublicationModelSite(PersonHistoryModelBase):
    model = Publication
    fields = ['title', 'description', 'publisher', 'date_published', 'document_link', 'privacy']


class FamilyModelSite(PersonHistoryModelBase):
    model = Family
    fields = ['relation', 'relationship', 'name', 'date_of_birth', 'place_of_birth', 'job', 'address', 'privacy']


class SkillModelSite(PersonHistoryModelBase):
    model = Skill
    fields = ['name', 'description', 'level', 'privacy']


class ProfileSiteGroup(ModelSiteGroup):
    namespace = 'profile'
    items = [
        PersonModelSite,
        PersonAddressModelSite,
        FormalEducationModelSite,
        NonFormalEducationModelSite,
        WorkingModelSite,
        VolunteerModelSite,
        AwardModelSite,
        PublicationModelSite,
        FamilyModelSite,
        SkillModelSite
    ]


profile_site = ProfileSiteGroup()
