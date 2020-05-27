from django.template import Library

from ..models.students import get_score_classname, get_score_status

register = Library()


@register.filter
def score_status(alphabetic):
    return get_score_status(alphabetic).title()


@register.filter
def score_classname(alphabetic):
    return get_score_classname(alphabetic)


@register.simple_tag(name='score_summary')
def score_summary(student, semester=None):
    semester_score = student.get_scores(semester=semester)
    return student.get_scores_summary(semester_score)