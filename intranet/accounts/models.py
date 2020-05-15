import uuid
from django.db import models
from django.db.utils import cached_property
from django.db.models.signals import post_save
from django.utils import translation
from django.shortcuts import reverse
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from django_personals.models import TitleMixin

from .gravatar import get_user_gravatar, get_gravatar_profile

_ = translation.ugettext_lazy


class User(TitleMixin, AbstractUser):
    avatar_size = 144
    avatar_default = '//www.gravatar.com/avatar/?s=288&d=mm'

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    email = models.EmailField(_('email address'), blank=False, unique=True)
    first_name = models.CharField(_('full name'), max_length=30, blank=False)

    is_superuser = models.BooleanField(
        _('superuser'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    is_staff = models.BooleanField(
        _('staff'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_student = models.BooleanField(
        _('student'),
        default=False,
        help_text=_('Designates whether the user is a student.'),
    )
    is_teacher = models.BooleanField(
        _('teacher'),
        default=False,
        help_text=_('Designates whether the user is a teacher.'),
    )
    is_employee = models.BooleanField(
        _('employee'),
        default=False,
        help_text=_('Designates whether the user is a employee.'),
    )
    is_management = models.BooleanField(
        _('management'),
        default=False,
        help_text=_('Designates whether the user is a management.'),
    )
    is_matriculant = models.BooleanField(
        _('matriculant'),
        default=False,
        help_text=_('Designates whether the user is a matriculant or student candidate.'),
    )
    is_applicant = models.BooleanField(
        _('applicant'),
        default=False,
        help_text=_('Designates whether the user is a employee or teacher applicant.'),
    )

    @property
    def is_insider(self):
        return self.is_academica or self.is_employee

    @property
    def is_academica(self):
        return self.is_valid_student or self.is_valid_teacher or self.is_management

    @property
    def is_valid_student(self):
        return self.is_student and self.students.count()

    @property
    def is_valid_teacher(self):
        return self.is_teacher and getattr(self, 'teacher', None)

    @property
    def is_valid_employee(self):
        return self.is_employee and getattr(self, 'employee', None)

    @cached_property
    def fullname_with_title(self):
        name = []
        if self.title and self.show_title:
            name.append(str(self.title) + '. ')
        if self.front_title and self.show_academic_title:
            name.append(str(self.front_title) + '. ')
        if self.get_full_name():
            name.append(self.get_full_name())
        if self.back_title and self.show_academic_title:
            name.append(', ' + str(self.back_title))
        return "".join(name)

    @cached_property
    def primary_email(self):
        allauth_emails = getattr(self, 'emailaddress_set', None)
        return allauth_emails.filter(primary=True).first()

    @cached_property
    def primary_student(self):
        return self.students.filter(primary=True).first()

    @cached_property
    def gravatar(self):
        url = get_user_gravatar(self)
        return self.avatar_default if not url else url

    @cached_property
    def gravatar_profile(self):
        return get_gravatar_profile(self.email)

    @cached_property
    def get_public_profile(self):
        return reverse('public_profile', args=(self.username,))

    def __str__(self):
        return self.fullname_with_title or self.username

    def natural_key(self):
        return (self.email,)

    @staticmethod
    def create_personal(sender, instance, created, **kwargs):
        from intranet.persons.models import Person
        if created:
            person = Person(account=instance)
            person.save()
        else:
            person, created = Person.objects.get_or_create(account=instance)
            person.save()


post_save.connect(User.create_personal, sender=User)
