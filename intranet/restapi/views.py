from django.contrib.auth import get_user_model

from rest_framework import viewsets

from ..accounts.serializers import UserSerializer
from ..academic.serializers import SchoolYearSerializer
from ..academic.models import SchoolYear


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class SchoolYearViewSet(viewsets.ModelViewSet):
    queryset = SchoolYear.objects.all()
    serializer_class = SchoolYearSerializer
