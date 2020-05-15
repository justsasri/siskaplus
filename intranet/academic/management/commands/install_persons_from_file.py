import os
import inspect
import pandas
from django.conf import settings
from django.apps import apps
from django.db import models
from django.db.utils import DatabaseError
from django.core.management.base import BaseCommand, CommandError
from django.core.serializers import base


class Command(BaseCommand):
    help = 'Import moels from CSV file'
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str)
        parser.add_argument('csv_file', type=str)
        parser.add_argument('--delimiter', type=str)
        parser.add_argument('--transaction', type=bool)

    def get_natural_keys(self, model):
        natural_keys = inspect.signature(
            model.objects.get_by_natural_key
        ).parameters.keys()
        return natural_keys

    def handle(self, *args, **options):

        # check model name
        model = options['model_name']
        opts = model.split('.')

        try:
            Model = apps.get_model(opts[0], opts[1])
        except:
            raise CommandError('Model not found "%s" does not exist' % opts)

        fields = {f.name: f for f in Model._meta.get_fields()}

        # Read CSV file
        file = os.path.join(settings.BASE_DIR, options['csv_file'])
        delimiter = options["delimiter"] or ";"
        dataframe = pandas.read_csv(
            filepath_or_buffer=file,
            delimiter=delimiter
        ).replace({pandas.np.nan: None})

        for rec in dataframe.to_dict(orient='record'):
            instance_data = {}
            # handle fields
            for name, value in rec.items():
                if value is None:
                    continue
                # Handle M2M relations
                field = fields[name]
                if field.remote_field and isinstance(field.remote_field, models.ManyToManyField):
                    # there is no ManyToManyField in CSV file
                    pass
                elif field.remote_field and isinstance(field.remote_field, models.ManyToOneRel):
                    # get concrete related object
                    field_model = field.remote_field.model
                    try:
                        natural_key = {key: value for key in self.get_natural_keys(field_model)}
                        instance_data[field.name] = field_model.objects.get_by_natural_key(**natural_key)
                    except field_model.DoesNotExist as err:
                        self.stdout.write('ERROR: %s %s.%s "%s}"' % (err, options["model_name"], name, value))
                else:
                    try:
                        instance_data[field.name] = field.to_python(value)
                    except Exception as e:
                        raise base.DeserializationError.WithData(e, Model._meta.model_name, rec['id'], value)

                        # Import action
                natural_key = {}

                for key in self.get_natural_keys(Model):
                    natural_key[key] = None if key not in instance_data else instance_data[key]

                if 'id' in instance_data:
                    natural_key['id'] = instance_data['id'].hex
                try:
                    instance, created = Model.objects.update_or_create(**natural_key, defaults=instance_data)
                    if created:
                        self.stdout.write('Creating "%s" succesfull ..' % str(instance))
                    else:
                        self.stdout.write('Updating "%s" succesfull ..' % str(instance))
                except DatabaseError as err:
                    self.stdout.write('ERROR: %s %s' % (err, [value for key, value in rec.items()]))

            self.stdout.write(self.style.SUCCESS('Import %s to % fisnihed.' % (file, model)))
