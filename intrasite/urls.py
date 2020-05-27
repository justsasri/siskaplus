from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls

from intranet.admin.sites import admin_site
from intranet.accounts import urls as accounts_urls
from intranet.academic.admin.sites import academic_admin
from intranet.academic.sites import academic_site
from intranet.lectures.sites import classroom_sites

urlpatterns = [

    url(r'^accounts/', include(accounts_urls)),
    url(r'^matriculant/', include('intranet.matriculants.urls')),

    url(r'^academic/', include(academic_site.get_urls())),
    url(r'^academic/admin/', academic_admin.urls),

    url(r'^classrooms/', include(classroom_sites.get_urls())),
    # url(r'^select2/', include('django_select2.urls')),
    url(r'^api/', include('intranet.restapi.urls')),
    url(r'^admin/', admin_site.urls),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += [
        # url(r'^__debug__/', include(debug_toolbar.urls)),
        url(r'^admin/docs/', include(admindocs_urls)),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # specific serving mechanism. This should be the last pattern in
    # the list:
]