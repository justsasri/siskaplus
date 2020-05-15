# Generated by Django 3.0.6 on 2020-05-08 12:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('intranet_academic', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='account',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='courses',
            field=models.ManyToManyField(blank=True, related_name='teachers', to='intranet_academic.Course', verbose_name='courses'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='rmu',
            field=models.ForeignKey(help_text='Teacher homebase.', limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to='intranet_academic.ManagementUnit', verbose_name='management unit'),
        ),
        migrations.AddField(
            model_name='student',
            name='account',
            field=models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL, verbose_name='Account'),
        ),
        migrations.AddField(
            model_name='student',
            name='coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='intranet_academic.Teacher', verbose_name='coach'),
        ),
        migrations.AddField(
            model_name='student',
            name='curriculum',
            field=models.ForeignKey(help_text='Student curriculum, important to maintain alumni curriculum', on_delete=django.db.models.deletion.PROTECT, to='intranet_academic.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AddField(
            model_name='student',
            name='rmu',
            field=models.ForeignKey(limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, to='intranet_academic.ManagementUnit', verbose_name='program study'),
        ),
        migrations.AddField(
            model_name='student',
            name='year_of_force',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intranet_academic.SchoolYear', verbose_name='year of force'),
        ),
        migrations.AddField(
            model_name='score',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_scores', to='intranet_academic.Course', verbose_name='Course'),
        ),
        migrations.AddField(
            model_name='score',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_intranet_academic.score_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='score',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='intranet_academic.Student', verbose_name='Student'),
        ),
        migrations.AddField(
            model_name='managementunit',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='intranet_academic.ManagementUnit', verbose_name='parent'),
        ),
        migrations.AddField(
            model_name='curriculumcourse',
            name='concentration',
            field=models.ManyToManyField(blank=True, related_name='curriculum_courses', to='intranet_academic.Concentration', verbose_name='concentration'),
        ),
        migrations.AddField(
            model_name='curriculumcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_courses', to='intranet_academic.Course', verbose_name='course'),
        ),
        migrations.AddField(
            model_name='curriculumcourse',
            name='curriculum',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_courses', to='intranet_academic.Curriculum', verbose_name='curriculum'),
        ),
        migrations.AddField(
            model_name='curriculum',
            name='rmu',
            field=mptt.fields.TreeForeignKey(help_text='Management Unit', limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, related_name='curriculums', to='intranet_academic.ManagementUnit', verbose_name='Program Study'),
        ),
        migrations.AddField(
            model_name='courserequisite',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisites', to='intranet_academic.Course', verbose_name='course'),
        ),
        migrations.AddField(
            model_name='courserequisite',
            name='requisite',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='required_by', to='intranet_academic.Course', verbose_name='requisite'),
        ),
        migrations.AddField(
            model_name='courseequalizer',
            name='new_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='new_equalizers', to='intranet_academic.CurriculumCourse', verbose_name='New Course'),
        ),
        migrations.AddField(
            model_name='courseequalizer',
            name='old_course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='old_equalizers', to='intranet_academic.CurriculumCourse', verbose_name='old course'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='intranet_academic.CourseGroup', verbose_name='course group'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='intranet_academic.CourseType', verbose_name='course type'),
        ),
        migrations.AddField(
            model_name='course',
            name='rmu',
            field=mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='courses', to='intranet_academic.ManagementUnit', verbose_name='management unit'),
        ),
        migrations.AddField(
            model_name='concentration',
            name='rmu',
            field=mptt.fields.TreeForeignKey(help_text='Management Unit', limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, related_name='concentrations', to='intranet_academic.ManagementUnit', verbose_name='Program Study'),
        ),
        migrations.AddField(
            model_name='academicyear',
            name='school_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intranet_academic.SchoolYear', verbose_name='school year'),
        ),
        migrations.AlterUniqueTogether(
            name='curriculumcourse',
            unique_together={('curriculum', 'course')},
        ),
        migrations.AlterUniqueTogether(
            name='courseequalizer',
            unique_together={('old_course', 'new_course')},
        ),
    ]
