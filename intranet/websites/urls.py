from django.urls import path, include
from rest_framework import routers

from intranet.restapi.views import academics


router = routers.DefaultRouter()
router.register(r'curriculums', academics.CurriculumViewsets)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
