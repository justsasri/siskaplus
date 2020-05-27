from functools import update_wrapper, wraps
from django.core.exceptions import ValidationError
from django.shortcuts import reverse, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect


def prevent_recursion(func):
    """ Decorator, Prevent Recursion inside Post Save Signal """

    @wraps(func)
    def no_recursion(sender, instance=None, **kwargs):
        if not instance:
            return
        # if there is _dirty, return
        if hasattr(instance, '_dirty'):
            return
        func(sender, instance=instance, **kwargs)
        try:
            # there is dirty, lets save
            instance._dirty = True
            instance.save()
        finally:
            del instance._dirty

    return no_recursion