from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password

from import_export.resources import ModelResource
from import_export import widgets, fields
from import_export.fields import Field

from ..core.resource_widgets import UUIDWidget


class UserResource(ModelResource):
    class Meta:
        model = get_user_model()
        fields = (
            'id', 'first_name', 'username', 'email', 'is_active',
            'is_student', 'is_teacher', 'is_employee', 'is_management',
            'is_matriculant', 'is_applicant'
        )

    id = Field(
        attribute='id',
        column_name='id',
        widget=UUIDWidget())
    first_name = Field(column_name='full_name', attribute='first_name')
    email = Field(column_name='email', attribute='email')
    new_password = Field(column_name='new_password', attribute='new_password')
    confirm_password = Field(column_name='confirm_password', attribute='confirm_password')
    password = Field(column_name='password', attribute='password', readonly=True)
    groups = fields.Field(
        column_name='group',
        attribute='groups',
        widget=widgets.ManyToManyWidget(Group, separator=',', field='name'))

    def check_confirm_password(self, psw, confirm):
        return psw == confirm

    def get_or_init_instance(self, instance_loader, row):
        """
        Either fetches an already existing user or initializes a new one.
        """
        new_password = row.pop('new_password')
        confirm_password = row.pop('confirm_password')
        if new_password != confirm_password:
            raise ValueError(_("Password doesn't match !"))

        instance = self.get_instance(instance_loader, row)
        if instance:
            instance.new_password = new_password
            instance.confirm_password = confirm_password
            return (instance, False)
        else:
            new_instance = self.init_instance(row)
            new_instance.new_password = new_password
            new_instance.confirm_password = confirm_password
            return (new_instance, True)

    def before_save_instance(self, instance, using_transactions, dry_run):
        """
        Set password if new one is available
        """
        if instance.new_password not in ['', None]:
            validate_password(instance.new_password, instance)
            instance.set_password(instance.new_password)
