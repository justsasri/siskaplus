from django.utils.translation import ugettext_lazy as _
from ...admin.sites import BaseAdminSite


class AcademicAdminSite(BaseAdminSite):
    site_url = '/academic/'
    site_title = _('Academic site admin')
    site_header = _('Academic Administration')
    index_title = _('Academic Administration')

    def has_permission(self, request):
        can_access_academic_admin = request.user.has_perm('global_permission.access_academic_admin')
        return request.user.is_superuser or (request.user.is_active and can_access_academic_admin)


academic_admin = AcademicAdminSite(name='academic_admin')
