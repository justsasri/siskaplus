# Generated by Django 3.0.6 on 2020-05-19 13:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet_academic', '0014_auto_20200519_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentscore',
            name='point',
            field=models.PositiveIntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='sks'),
        ),
    ]
