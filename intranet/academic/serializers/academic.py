from rest_framework.serializers import ModelSerializer

from ..models import (
    SchoolYear
)

class SchoolYearSerializer(ModelSerializer):
    class Meta:
        model = SchoolYear
        fields = ('url', 'id', 'code', 'year_start', 'year_end')