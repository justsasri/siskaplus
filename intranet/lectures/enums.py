import enum
from django.utils.translation import ugettext_lazy as _


class LectureStatus(enum.Enum):
    DRAFT = 'DRF'  # Lectures state in draft
    PUBLISHED = 'PUB'  # Lectures is visible for registration
    ARCHIVED = 'ACF'  # Registration closed, and operator preparing lecture, eg. assign student, schedule etc.
    TRASH = 'TRS'  # Registration closed, and operator preparing lecture, eg. assign student, schedule etc.

    CHOICES = (
        (DRAFT, _('draft').title()),
        (PUBLISHED, _('published').title()),
        (ARCHIVED, _('archived').title()),
        (TRASH, _('trash').title()),
    )


class LectureType(enum.Enum):
    MEETING = '1'
    ELEARNING = '2'
    MID_EXAM = '3'
    FINAL_EXAM = '4'
    SUBTITUTE = '99'
    CHOICES = (
        (MEETING, _('Meeting')),
        (ELEARNING, _('E-Learning')),
        (SUBTITUTE, _('Subtitution')),
        (MID_EXAM, _('Mid Exam')),
        (FINAL_EXAM, _('Final Exam')),
    )


class EnrollmentItemMark(enum.Enum):
    CHECK = 'CHECK'
    VALID = 'VALID'
    DELETED = 'DELETED'

    CHOICES = (
        (CHECK, _('Check')),
        (VALID, _('Valid')),
        (DELETED, _('Deleted')),
    )


class EnrollmentCriteria(enum.Enum):
    NEW = '1'
    REMEDY = '2'


class AttendantStatus(enum.Enum):
    PRESENT = 'PR'
    SICK = 'SC'
    ABSENT = 'AB'
    PERMIT = 'PE'