import uuid
from django.db import models
from django.utils import translation, timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from .managers import BaseManager

_ = translation.gettext_lazy


class BaseModel(models.Model):
    class Meta:
        abstract = True

    objects = BaseManager()

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        verbose_name='uuid')
    is_trash = models.BooleanField(
        default=False,
        editable=False,
        verbose_name=_('trash'))
    trashed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        editable=False,
        null=True, blank=True,
        related_name="%(class)s_trashes",
        on_delete=models.CASCADE,
        verbose_name=_('trashed by'))
    trashed_at = models.DateTimeField(
        null=True, blank=True, editable=False)

    def pass_delete_validation(self):
        return True

    def get_deletion_error_message(self):
        return _("E1001: %s deletion can't be performed.") % self._meta.verbose_name

    def get_deletion_message(self):
        return _("E1010: %s deletion can't be performed.") % self._meta.verbose_name

    def delete(self, using=None, keep_parents=False, paranoid=False, user=None):
        """
            Give paranoid delete mechanism to each record
        """
        if not self.pass_delete_validation():
            raise ValidationError(self.get_deletion_error_message())

        if paranoid:
            self.is_trash = True
            self.trashed_by = user
            self.trashed_at = timezone.now()
            self.save()
        else:
            super().delete(using=using, keep_parents=keep_parents)

    def pass_restore_validation(self):
        return self.is_trash

    def get_restoration_error_message(self):
        return _("E1002: %s restoration can't be performed.") % self._meta.verbose_name

    def restore(self):
        if not self.pass_restore_validation():
            raise ValidationError(self.get_restoration_error_message())

        self.is_trash = False
        self.trashed_by = None
        self.trashed_at = None
        self.save()
