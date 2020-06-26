from rest_framework import viewsets

from intranet.restapi.serializers.academics import CurriculumSerializer
from intranet.academic.models import Curriculum

class CurriculumViewsets(
        viewsets.mixins.ListModelMixin,
        viewsets.GenericViewSet):

    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer