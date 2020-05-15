from django.db import models
from ..academic.enums import KKNILevel


class DepartmentManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset().select_related('parent')
        return qs


class PositionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('department', 'parent')


class EmployeeManager(models.Manager):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('account', 'position', 'employment')

    def get_summary(self):
        from .models import Employment
        kontrak, created = Employment.objects.get_or_create(name='Kontrak', defaults={'name': 'Kontrak'})
        tetap, created = Employment.objects.get_or_create(name='Tetap', defaults={'name': 'Tetap'})
        outsource, created = Employment.objects.get_or_create(name='Outsource', defaults={'name': 'Outsource'})
        return self.get_queryset().aggregate(
            count_total=models.Count('id'),
            count_active=models.Count('id', filter=models.Q(is_active=True)),
            count_inactive=models.Count('id', filter=models.Q(is_active=False)),
            count_kontrak=models.Count('id', filter=models.Q(employment=kontrak)),
            count_tetap=models.Count('id', filter=models.Q(employment=tetap)),
            count_outsource=models.Count('id', filter=models.Q(employment=outsource)),
            count_sma_active=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.SD.value, KKNILevel.SMP.value, KKNILevel.SMA.value
                    ]) & models.Q(is_active=True)
            ),
            count_sma_inactive=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.SD.value, KKNILevel.SMP.value, KKNILevel.SMA.value
                    ]) & models.Q(is_active=False)
            ),
            count_d3_active=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.D3.value, KKNILevel.D2.value, KKNILevel.D1.value
                    ]) & models.Q(is_active=True)
            ),
            count_d3_inactive=models.Count(
                'id', filter=models.Q(
                    person__last_education_level__in=[
                        KKNILevel.D3.value, KKNILevel.D2.value, KKNILevel.D1.value
                    ]) & models.Q(is_active=False)
            ),
            count_s1_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S1.value) & models.Q(is_active=True)
            ),
            count_s1_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S1.value) & models.Q(is_active=False)
            ),
            count_s2_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S2.value) & models.Q(is_active=True)
            ),
            count_s2_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S2.value) & models.Q(is_active=False)
            ),
            count_s3_active=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S3.value) & models.Q(is_active=True)
            ),
            count_s3_inactive=models.Count(
                'id', filter=models.Q(person__last_education_level=KKNILevel.S3.value) & models.Q(is_active=False)
            ),
        )

    def get_by_natural_key(self, eid):
        return self.get(eid=eid)


class ExtraPositionManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related('position', 'employee')
