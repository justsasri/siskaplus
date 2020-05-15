from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a student,
        redirects to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_student,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a teacher,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_teacher,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def management_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a management,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_management,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def academica_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a management,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_academica,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def employee_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a employee,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_employee,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def insider_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a employee,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_employee,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def applicant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a employee,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_applicant,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def matriculant_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='account_login'):
    """
        Decorator for views that checks that the logged in user is a matriculant,
        redirects to the log-in page if necessary.
    """

    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_matriculant,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
