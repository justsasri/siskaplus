import inspect
import functools
from django.apps import apps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from django.urls import NoReverseMatch, reverse, include, path
from django.shortcuts import Http404
from django.template.response import TemplateResponse
from django.contrib.admin.sites import AdminSite

def is_class_based_view(view):
    return inspect.isclass(view) and issubclass(view, View)

class AdminPlusMixin(object):
    """ Thanks To django-admin plus
        Mixin for AdminSite to allow registering custom admin views.
        https://github.com/jsocol/django-adminplus
    """

    custom_views = []
    app_views = []

    def wrap_view(self, view):
        def wrapper(*args, **kwargs):
            return self.admin_view(view)(*args, **kwargs)

        wrapper.model_admin = self
        return functools.update_wrapper(wrapper, view)

    def register_site_view(self, path, name=None, urlname=None, visible=True,
                           view=None):
        """Add a custom admin view. Can be used as a function or a decorator.
        * `path` is the path in the admin where the view will live, e.g.
            http://example.com/admin/somepath
        * `name` is an optional pretty name for the list of custom views. If
            empty, we'll guess based on view.__name__.
        * `urlname` is an optional parameter to be able to call the view with a
            redirect() or reverse()
        * `visible` is a boolean or predicate returning one, to set if
            the custom view should be visible in the admin dashboard or not.
        * `view` is any view function you can imagine.
        Example :
        ```
        @admin_site.register_view('someview',
                         name='Some View',
                         urlname='some_view',
                         visible=False)
        def my_view(request):
            from  django.http import HttpResponse
            return HttpResponse('Custom View')```
        """

        def decorator(fn):
            if is_class_based_view(fn):
                fn = fn.as_view()
            self.custom_views.append((path, fn, name, urlname, visible))
            return fn

        if view is not None:
            decorator(view)
            return

        return decorator

    def register_app_view(self, app_view):
        """ Add a custom admin app view. Can be used as a function or a decorator. """
        admin_site = self

        def decorator(cls):
            self.app_views.append(cls(admin_site))
            return cls(admin_site)

        if app_view is not None:
            decorator(app_view)
            return
        return decorator

    def get_urls(self):
        """Add our custom views to the admin urlconf."""
        urls = super().get_urls()
        for viewpath, view, name, urlname, visible in self.custom_views:
            urls = [path('%s/' % viewpath, self.admin_view(view), name=urlname)] + urls
        for app_view in self.app_views:
            urls = [path('%s/%s/' % app_view.info, include(app_view.urls))] + urls
        return urls

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.
        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        # get each context from super
        each_ctx = super().each_context(request)

        each_ctx['custom_view_list'] = self.get_custom_view_list(request)
        each_ctx['custom_app_list'] = self.get_custom_app_list(request)
        return each_ctx

    def _build_app_dict(self, request, label=None):
        """ Modify app dict to add custom app view after model list """

        app_dict = super()._build_app_dict(request, label=None)

        # add custom app view after model
        for app_view in self.app_views:
            if app_view.app_label in app_dict and app_view.show_in_index:
                view_list = app_dict[app_view.app_label]['models']
                view_dict = {
                    'name': capfirst(app_view.name),
                    'object_name': '',
                    'perms': True,
                    'admin_url': None,
                    'add_url': None,
                    'view_only': True,
                }
                try:
                    view_name = 'admin:{}_{}_index'.format(app_view.app_label, app_view.base_path)
                    view_dict['admin_url'] = reverse(view_name)
                except NoReverseMatch:
                    pass
                view_list.append(view_dict)

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site and add icon.
        """
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # set auth app icon
        authConfig = apps.get_app_config('auth')
        setattr(authConfig, 'mdicon', 'mdi-clipboard-account')

        for app in app_list:
            appConfig = apps.get_app_config(app['app_label'])
            if not hasattr(appConfig, 'mdicon'):
                setattr(appConfig, 'mdicon', '')
            app['icon'] = appConfig.mdicon
            # Sort the models alphabetically within each app.
            # app['models'].sort(key=lambda x: x['name'])
        return app_list

    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        # Sort the models alphabetically within each app.
        # app_dict['models'].sort(key=lambda x: x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)

    def get_custom_app_list(self, request):
        """ Return app list for each path, replace context processor capability """
        app_list = self.get_app_list(request)
        return app_list

    def get_custom_view_list(self, request):
        """ Return list of custom view """
        custom_views = self.custom_views
        view_list = []
        for path, view, name, urlname, visible in custom_views:
            urlname = '%s:%s' % (self.name, urlname)
            if callable(visible):
                visible = visible(request)
            if visible:
                if name:
                    view_list.append((path, name, urlname))
                else:
                    view_list.append((path, capfirst(view.__name__), urlname))

        # Sort views alphabetically.
        view_list.sort(key=lambda x: x[1])
        return view_list


class BaseAdminSite(AdminPlusMixin, AdminSite):
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
        return functools.update_wrapper(inner, view)

    @never_cache
    def login(self, request, extra_context=None):
        return redirect(reverse('account_login'))

    @never_cache
    def logout(self, request, extra_context=None):
        return redirect(reverse('account_logout'))


class IntranetAdminSite(BaseAdminSite):
    site_title = _('Intranet admin')
    site_header = _('Intranet Administration')
    index_title = _('Intranet Administration')


admin_site = IntranetAdminSite(name='admin')