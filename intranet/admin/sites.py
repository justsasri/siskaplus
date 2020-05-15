from functools import update_wrapper
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.contrib.admin.sites import AdminSite
from django.utils.translation import ugettext_lazy as _


class BaseAdminSite(AdminSite):
    site_title = _('Custom admin')
    site_header = _('Custom Administration')
    index_title = _('Custom Administration')

    def has_permission(self, request):
        return request.user.is_active

    def admin_view(self, view, cacheable=False):
        """
        Override default redirect_to_login url
        """
        def inner(request, *args, **kwargs):
            from django.contrib.auth.views import redirect_to_login
            if not request.user.is_authenticated:
                return redirect_to_login(
                    request.get_full_path(),
                    reverse('account_login')  # <--- This Line
                )
            if not self.has_permission(request):
                return HttpResponseForbidden("<h1>Sorry, You don't have any permissions.<h1>")
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    @never_cache
    def login(self, request, extra_context=None):
        return redirect(reverse('account_login'))

    @never_cache
    def logout(self, request, extra_context=None):
        return redirect(reverse('account_logout'))
