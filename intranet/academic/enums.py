import enum
from django.utils.translation import ugettext_lazy as _


class AcademicStatus(enum.Enum):
    PENDING = 'PND'
    ONGOING = 'ONG'
    END = 'END'

    CHOICES = (
        (PENDING, _('pending').title()),
        (ONGOING, _('on going').title()),
        (END, _('ended').title()),
    )


class ManagementLevel(enum.Enum):
    UNIVERSITY = 1
    FACULTY = 2
    MAJOR = 3
    PROGRAM_STUDY = 4

    CHOICES = (
        (UNIVERSITY, _('university').title()),
        (FACULTY, _('faculty').title()),
        (MAJOR, _('major').title()),
        (PROGRAM_STUDY, _('program study').title()),
    )


class Semester(enum.Enum):
    ODD = 1
    EVEN = 2
    SHORT = 3

    CHOICES = (
        (ODD, _('odd').title()),
        (EVEN, _('even').title()),
        (SHORT, _('short').title()),
    )


class KKNILevel(enum.Enum):
    SD = 0  # <-- elementary
    SMP = 1  # <-- junior high school
    SMA = 2  # <-- junior high school
    D1 = 3  # <-- diploma
    D2 = 4
    D3 = 5
    D4 = 6
    S1 = 7  # <-- bachelor
    S2 = 8  # <-- master
    S3 = 9  # <-- doctor

    CHOICES = (
        (0, _('SD')),
        (1, _('SMP')),
        (2, _('SMA')),
        (3, _('D1')),
        (4, _('D2')),
        (5, _('D3')),
        (6, _('D4')),
        (7, _('S1')),
        (8, _('S2')),
        (9, _('S3')),
    )

    UNIVERSITY = (
        (5, _('D3')),
        (7, _('S1')),
        (8, _('S2')),
        (9, _('S3')),
    )


class StudentStatus(enum.Enum):
    ACTIVE = 'ACT'
    ALUMNI = 'ALM'
    DROP_OUT = 'DRO'
    MOVED = 'MVD'
    MISC = 'MSC'

    CHOICES = (
        (ACTIVE, _('active').title()),
        (ALUMNI, _('alumni').title()),
        (DROP_OUT, _('drop out').title()),
        (MOVED, _('moved').title()),
        (MISC, _('misc').title()),
    )
