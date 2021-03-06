# Generated by Django 3.0.6 on 2020-05-16 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet_lectures', '0003_auto_20200516_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrollment',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='enrollmentitem',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='lectureschedule',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='lecturescoreweighting',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='lecturestudent',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='studentattendance',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='studentplan',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
        migrations.AlterField(
            model_name='teacherattendance',
            name='is_trash',
            field=models.BooleanField(default=False, editable=False, verbose_name='trash'),
        ),
    ]
