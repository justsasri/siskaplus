from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls

# Web API
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from intranet.admin.sites import admin_site
from intranet.core.views import HomePageView
from intranet.accounts import urls as accounts_urls
from intranet.academic.admin.sites import academic_admin
from intranet.academic.sites import academic_site
from intranet.lectures.sites import classroom_sites

schema_view = get_schema_view(
   openapi.Info(
      title="Darmajaya Web API",
      default_version='v1',
      description="Darmajaya Information System API",
      terms_of_service="https://www.darmajaya.net/privacy_policy/",
      contact=openapi.Contact(email="sasri.darmajaya@gmail"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
api_doc = schema_view.with_ui('redoc', cache_timeout=0)

urlpatterns = [

    path('', HomePageView.as_view()),
    path('accounts/', include(accounts_urls)),
    path('matriculant/', include('intranet.matriculants.urls')),
    path('academic/', include(academic_site.get_urls())),
    path('classrooms/', include(classroom_sites.get_urls())),
    
    # Plugin
    # path('select2/', include('django_select2.urls')),
    
    # Web API
    path('api/', include('intranet.restapi.urls')),
    path('apidoc/', api_doc),
    
    # Admin
    path('admin/', admin.site.urls),
    path('academic/admin/', academic_admin.urls),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    import debug_toolbar

    # Serve static and media files from development server
    urlpatterns += [
        # path('__debug__/', include(debug_toolbar.urls)),
        path('admin/docs/', include(admindocs_urls)),
    ]
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # specific serving mechanism. This should be the last pattern in
    # the list:
]