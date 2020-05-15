import uuid
from django.db import models, transaction
from django.db.utils import cached_property
from django.utils import translation, timezone, text
from django.conf import settings
from django.shortcuts import reverse

from django_numerators.models import NumeratorMixin
from django_personals.models import (
    TitleMixin, PersonAbstract, ContactAbstract, AddressAbstract, SocialAbstract,
    SkillAbstract, AwardAbstract, FormalEduAbstract, NonFormalEduAbstract, WorkingAbstract,
    VolunteerAbstract, PublicationAbstract, FamilyAbstract)

from ...core.enums import MaxLength
from ...academic.enums import KKNILevel

_ = translation.gettext_lazy


class PersonManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_employee(self):
        return self.filter(employee__isnull=False)

    def get_customer(self):
        return self.filter(partners__is_customer=True)

    def get_vendor(self):
        return self.filter(partners__is_vendor=True)


class Person(NumeratorMixin, PersonAbstract):
    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        permissions = (
            ('export_person', 'Can export Person'),
            ('import_person', 'Can import Person'),
            ('change_status_person', 'Can change status Person')
        )

    objects = PersonManager()

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('User account'))

    # Last Education
    education_level = models.PositiveIntegerField(
        choices=KKNILevel.CHOICES.value,
        default=KKNILevel.SMA.value,
        verbose_name=_('Level'))
    education_institution = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Institution'))
    education_name = models.CharField(
        null=True, blank=True,
        max_length=MaxLength.MEDIUM.value,
        verbose_name=_('Major'))
    year_graduate = models.IntegerField(
        null=True, blank=True, verbose_name=_('year graduate'))

    def __str__(self):
        return str(self.account)


class Contact(ContactAbstract):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE)


class SocialMedia(SocialAbstract):
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE)


class ModelURLMixin(models.Model):
    class Meta:
        abstract = True

    def get_edit_url(self):
        return reverse('profile_%s_edit' % self._meta.model_name, args=(self.pk,))

    def get_delete_url(self):
        return reverse('profile_%s_delete' % self._meta.model_name, args=(self.pk,))


class PersonAddress(ModelURLMixin, AddressAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='addresses'
    )


class Skill(ModelURLMixin, SkillAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='skills'
    )

    def __str__(self):
        return self.name


class Award(ModelURLMixin, AwardAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='awards'
    )

    def __str__(self):
        return self.name


class FormalEducation(ModelURLMixin, FormalEduAbstract):
    level = models.PositiveIntegerField(
        choices=KKNILevel.CHOICES.value,
        default=KKNILevel.S1.value,
        verbose_name=_('level'))
    person = models.ForeignKey(
        Person, null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='formal_educations'
    )

    def __str__(self):
        return self.institution


class NonFormalEducation(ModelURLMixin, NonFormalEduAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='non_formal_educations'
    )

    def __str__(self):
        return self.name


class Working(ModelURLMixin, WorkingAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='work_histories'
    )

    def __str__(self):
        return self.name


class Volunteer(ModelURLMixin, VolunteerAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='volunteers'
    )

    def __str__(self):
        return self.organization


class Publication(ModelURLMixin, PublicationAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='publications'
    )

    def __str__(self):
        return self.title


class Family(ModelURLMixin, FamilyAbstract):
    person = models.ForeignKey(
        Person, on_delete=models.CASCADE,
        related_name='families'
    )

    def __str__(self):
        return self.name
