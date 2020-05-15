import enum
from django.utils.translation import ugettext_lazy as _


class MaxLength(enum.Enum):
    SHORT = 128
    MEDIUM = 256
    LONG = 512
    XLONG = 1024
    TEXT = 2048
    RICHTEXT = 10000


class ActiveStatus(enum.Enum):
    ACTIVE = 'ACT'
    INACTIVE = 'INC'

    CHOICES = (
        (ACTIVE, _("active").title()),
        (INACTIVE, _("inactive").title()),
    )


class PrivacyStatus(enum.Enum):
    ANYONE = 'anyone'
    USERS = 'users'
    FRIENDS = 'friends'
    STUDENTS = 'students'
    TEACHERS = 'teachers'
    EMPLOYEES = 'employees'
    MANAGERS = 'managers'
    ME = 'me'

    CHOICES = (
        (ANYONE, _("anyone").title()),
        (USERS, _('all users').title()),
        (FRIENDS, _('all friends').title()),
        (STUDENTS, _('all students').title()),
        (TEACHERS, _('all teachers').title()),
        (EMPLOYEES, _('all employees').title()),
        (MANAGERS, _('all managers').title()),
        (ME, _('only me').title())
    )

class DVCPStatus(enum.Enum):
    DRAFT = 'DRF'
    VALID = 'VLD'
    CANCELED = 'CNC'
    POSTED = 'PST'

    CHOICES = (
        (DRAFT, _('draft').title()),
        (VALID, _('valid').title()),
        (POSTED, _('posted').title()),
        (CANCELED, _('cancel').title()),
    )