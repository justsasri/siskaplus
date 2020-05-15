from django.urls import path
from allauth import urls as allauth_urls

from .sites import profile_site, student_site
from .views import AccountHomeView

accounts_urls = allauth_urls.urlpatterns

urlpatterns = accounts_urls + [
    path('', AccountHomeView.as_view(), name='account_home'),
] + profile_site.get_urls() + student_site.get_urls()
