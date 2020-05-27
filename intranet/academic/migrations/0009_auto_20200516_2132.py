# Generated by Django 3.0.6 on 2020-05-16 14:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet_academic', '0008_auto_20200516_2125'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scorerange',
            options={'ordering': ['schema', 'alphabetic'], 'verbose_name': 'Score Range', 'verbose_name_plural': 'Score Ranges'},
        ),
        migrations.AlterField(
            model_name='conversionstudentscore',
            name='ori_numeric_score',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Origin Numeric'),
        ),
        migrations.AlterField(
            model_name='scorerange',
            name='numeric',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Numeric Score'),
        ),
        migrations.AlterField(
            model_name='studentconversionitem',
            name='numeric',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Numeric Score'),
        ),
        migrations.AlterField(
            model_name='studentconversionitem',
            name='ori_numeric',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(4)], verbose_name='Origin Numeric'),
        ),
    ]
