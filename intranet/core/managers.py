from django.db import models
from django.db.models.functions import Coalesce
from django.utils import translation

_ = translation.gettext_lazy


def count_subquery(model, extra_filter=None):
    filter = {'rmu_id': models.OuterRef('pk')}
    if extra_filter:
        filter.update(extra_filter)
    sqs = Coalesce(
        models.Subquery(
            model.objects.filter(**filter).order_by().values('rmu_id').annotate(
                total=models.Count('*')
            ).values('total'),
            output_field=models.IntegerField()
        ), 0)
    return sqs


def cumulative_count_subquery(model, extra_filter=None):
    filter = {
        'rmu__tree_id': models.OuterRef('tree_id'),
        'rmu__lft__gte': models.OuterRef('lft'),
        'rmu__lft__lte': models.OuterRef('rght')
    }
    if extra_filter:
        filter.update(extra_filter)
    sqs = Coalesce(
        models.Subquery(
            model.objects.filter(
                **filter
            ).order_by().values('rmu__tree_id').annotate(
                total=models.Count('*')
            ).values('total'),
            output_field=models.IntegerField()
        ), 0)
    return sqs


class BaseManager(models.Manager):
    """
        Implement paranoid mechanism queryset
    """

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get(self, *args, **kwargs):
        kwargs['is_deleted'] = False
        return super().get(*args, **kwargs)
