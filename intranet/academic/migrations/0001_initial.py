# Generated by Django 3.0.6 on 2020-05-15 03:52

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concentration',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.SlugField(blank=True, max_length=3, null=True, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'concentration',
                'verbose_name_plural': 'concentrations',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('old_code', models.CharField(help_text='Maintain legacy system data integrity', max_length=256, null=True, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('level', models.PositiveIntegerField(choices=[(5, 'D3'), (7, 'S1'), (8, 'S2'), (9, 'S3')], default=7, verbose_name='level')),
                ('year_offered', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4')], default=1, verbose_name='year offered')),
                ('summary', models.CharField(blank=True, max_length=256, null=True, verbose_name='summary')),
                ('description', models.TextField(blank=True, max_length=10000, null=True, verbose_name='description')),
                ('meeting', models.PositiveIntegerField(default=0, verbose_name='Meeting')),
                ('practice', models.PositiveIntegerField(default=0, verbose_name='Practice')),
                ('field_practice', models.PositiveIntegerField(default=0, verbose_name='Field')),
                ('simulation', models.PositiveIntegerField(default=0, verbose_name='Simulation')),
                ('total', models.PositiveIntegerField(default=0, editable=False, verbose_name='Total')),
                ('learning_program', models.URLField(blank=True, help_text='Lecture Program Unit a.k.a SAP', null=True, verbose_name='learning program')),
                ('dictate', models.URLField(blank=True, null=True, verbose_name='dictate')),
                ('teaching_material', models.URLField(blank=True, null=True, verbose_name='teaching material')),
                ('practice_program', models.URLField(blank=True, null=True, verbose_name='practice program')),
                ('syllabus', models.URLField(blank=True, null=True, verbose_name='syllabus')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('is_public', models.BooleanField(default=True, verbose_name='Public')),
            ],
            options={
                'verbose_name': 'course',
                'verbose_name_plural': 'courses',
                'ordering': ('inner_id',),
            },
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')], default=1, unique=True, verbose_name='Code')),
                ('name', models.CharField(max_length=512, verbose_name='Name')),
                ('alias', models.CharField(blank=True, max_length=512, null=True, verbose_name='Alias')),
            ],
            options={
                'verbose_name': 'course group',
                'verbose_name_plural': 'course groups',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='CourseType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')], default=1, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=512, verbose_name='name')),
                ('alias', models.CharField(blank=True, max_length=512, null=True, verbose_name='alias')),
            ],
            options={
                'verbose_name': 'course type',
                'verbose_name_plural': 'course types',
                'ordering': ('code',),
            },
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.CharField(max_length=256, unique=True, verbose_name='code')),
                ('year', models.CharField(choices=[('2010', '2010'), ('2011', '2011'), ('2012', '2012'), ('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026'), ('2027', '2027'), ('2028', '2028'), ('2029', '2029')], default='2019', max_length=4, verbose_name='year')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('sks_graduate', models.PositiveIntegerField(default=0, verbose_name='SKS graduate')),
                ('summary', models.CharField(blank=True, max_length=256, null=True, verbose_name='summary')),
                ('description', models.TextField(blank=True, max_length=10000, null=True, verbose_name='description')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_public', models.BooleanField(default=True, verbose_name='public')),
                ('is_primary', models.BooleanField(default=False, verbose_name='primary')),
            ],
            options={
                'verbose_name': 'Curriculum',
                'verbose_name_plural': 'Curriculums',
            },
        ),
        migrations.CreateModel(
            name='ManagementUnit',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('type', models.IntegerField(choices=[(1, 'University'), (2, 'Faculty'), (3, 'Major'), (4, 'Program Study')], default=1, verbose_name='type')),
                ('number', models.CharField(blank=True, max_length=3, null=True, verbose_name='number')),
                ('code', models.SlugField(max_length=3, unique=True, verbose_name='code')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='childrens', to='intranet_academic.ManagementUnit', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'management unit',
                'verbose_name_plural': 'management units',
            },
        ),
        migrations.CreateModel(
            name='SchoolYear',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.CharField(editable=False, max_length=256, unique=True, verbose_name='code')),
                ('year_start', models.IntegerField(choices=[(2010, '2010'), (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'), (2025, '2025'), (2026, '2026'), (2027, '2027'), (2028, '2028'), (2029, '2029')], default=2019, verbose_name='year start')),
                ('year_end', models.IntegerField(choices=[(2010, '2010'), (2011, '2011'), (2012, '2012'), (2013, '2013'), (2014, '2014'), (2015, '2015'), (2016, '2016'), (2017, '2017'), (2018, '2018'), (2019, '2019'), (2020, '2020'), (2021, '2021'), (2022, '2022'), (2023, '2023'), (2024, '2024'), (2025, '2025'), (2026, '2026'), (2027, '2027'), (2028, '2028'), (2029, '2029')], default=2020, verbose_name='year end')),
            ],
            options={
                'verbose_name': 'school year',
                'verbose_name_plural': 'school years',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('student_id', models.CharField(blank=True, max_length=128, null=True, verbose_name='student ID')),
                ('registration_id', models.CharField(max_length=128, null=True, verbose_name='registration ID')),
                ('registration', models.PositiveIntegerField(choices=[(1, 'Reguler'), (2, 'Transfer')], default=1, verbose_name='registration')),
                ('semester', models.PositiveIntegerField(default=0, help_text='Student semester number, updated automatically when student create enrollment document ', verbose_name='Semester')),
                ('primary', models.BooleanField(default=False, help_text='Mark as primary student object, used when login', verbose_name='primary')),
                ('status', models.CharField(choices=[('ACT', 'Active'), ('ALM', 'Alumni'), ('DRO', 'Drop Out'), ('MVD', 'Moved'), ('MSC', 'Misc')], default='ACT', max_length=128, verbose_name='status')),
                ('status_note', models.CharField(blank=True, max_length=256, null=True, verbose_name='status note')),
                ('account', models.ForeignKey(limit_choices_to={'is_student': True}, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL, verbose_name='Account')),
            ],
            options={
                'verbose_name': 'student',
                'verbose_name_plural': 'students',
                'permissions': (('register_student', 'Can Register New Student'),),
            },
        ),
        migrations.CreateModel(
            name='StudentConversion',
            fields=[
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('ori_institution_name', models.CharField(help_text='Institusi asal', max_length=256, verbose_name='Institution Name')),
                ('ori_program_study', models.CharField(help_text='Program Studi asal', max_length=256, verbose_name='Program Study')),
                ('ori_year_of_force', models.PositiveIntegerField(default=2010, help_text='Tahun masuk/angkatan pada institusi asal', validators=[django.core.validators.MinValueValidator(2000), django.core.validators.MaxValueValidator(2100)], verbose_name='Year of force')),
                ('status', models.CharField(choices=[('DRF', 'Draft'), ('VLD', 'Valid'), ('PST', 'Posted'), ('CNC', 'Cancel')], default='DRF', max_length=128, verbose_name='Status')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversions', to='intranet_academic.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Student Conversion',
                'verbose_name_plural': 'Student Conversions',
            },
        ),
        migrations.CreateModel(
            name='StudentScore',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('numeric', models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Numeric Score')),
                ('alphabetic', models.CharField(max_length=1, verbose_name='Alphabetic Score')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='course_scores', to='intranet_academic.Course', verbose_name='Course')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_intranet_academic.studentscore_set+', to='contenttypes.ContentType')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='intranet_academic.Student', verbose_name='Student')),
            ],
            options={
                'verbose_name': 'Score',
                'verbose_name_plural': 'Scores',
            },
        ),
        migrations.CreateModel(
            name='ConversionStudentScore',
            fields=[
                ('studentscore_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='intranet_academic.StudentScore')),
                ('ori_code', models.CharField(max_length=128, verbose_name='Origin Code')),
                ('ori_name', models.CharField(max_length=128, verbose_name='Origin Name')),
                ('ori_numeric_score', models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Origin Numeric')),
                ('ori_alphabetic_score', models.CharField(max_length=128, verbose_name='Origin Alphabetic')),
            ],
            options={
                'verbose_name': 'Conversion Student Score',
                'verbose_name_plural': 'Conversion Student Scores',
            },
            bases=('intranet_academic.studentscore',),
        ),
        migrations.CreateModel(
            name='PlainStudentScore',
            fields=[
                ('studentscore_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='intranet_academic.StudentScore')),
            ],
            options={
                'verbose_name': 'Plain Student Score',
                'verbose_name_plural': 'Plain Student Scores',
            },
            bases=('intranet_academic.studentscore',),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('tid', models.CharField(help_text='Provide NIDN or Employee ID', max_length=128, null=True, unique=True, verbose_name='teacher ID')),
                ('is_active', models.BooleanField(default=True, verbose_name='active status')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Account')),
                ('courses', models.ManyToManyField(blank=True, related_name='teachers', to='intranet_academic.Course', verbose_name='courses')),
                ('rmu', models.ForeignKey(help_text='Teacher homebase.', limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, related_name='teachers', to='intranet_academic.ManagementUnit', verbose_name='management unit')),
            ],
            options={
                'verbose_name': 'teacher',
                'verbose_name_plural': 'teachers',
            },
        ),
        migrations.CreateModel(
            name='StudentConversionItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('ori_code', models.CharField(max_length=128, verbose_name='Origin Code')),
                ('ori_name', models.CharField(max_length=128, verbose_name='Origin Name')),
                ('ori_numeric_score', models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Origin Numeric')),
                ('ori_alphabetic_score', models.CharField(max_length=128, verbose_name='Origin Alphabetic')),
                ('numeric', models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], verbose_name='Numeric Score')),
                ('alphabetic', models.CharField(max_length=1, verbose_name='Alphabetic Score')),
                ('conversion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conversion_items', to='intranet_academic.StudentConversion', verbose_name='Conversion')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='conversion_items', to='intranet_academic.Course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Student Conversion Score',
                'verbose_name_plural': 'Student Conversion Scores',
            },
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
        migrations.CreateModel(
            name='CurriculumCourse',
            fields=[
                ('reg_number', models.PositiveIntegerField(blank=True, editable=False, null=True, verbose_name='Reg number')),
                ('inner_id', models.CharField(blank=True, editable=False, max_length=50, null=True, unique=True, verbose_name='Inner ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='created at')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('semester_number', models.PositiveIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8')], default=1, null=True, verbose_name='semester')),
                ('sks_graduate', models.PositiveIntegerField(blank=True, help_text='Minimum sks graduated to enroll this course', null=True, verbose_name='SKS graduate')),
                ('concentration', models.ManyToManyField(blank=True, related_name='curriculum_courses', to='intranet_academic.Concentration', verbose_name='concentration')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_courses', to='intranet_academic.Course', verbose_name='course')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='curriculum_courses', to='intranet_academic.Curriculum', verbose_name='curriculum')),
            ],
            options={
                'verbose_name': 'curricullum course',
                'verbose_name_plural': 'curricullum courses',
                'ordering': ('curriculum', 'semester_number'),
                'unique_together': {('curriculum', 'course')},
            },
        ),
        migrations.AddField(
            model_name='curriculum',
            name='rmu',
            field=mptt.fields.TreeForeignKey(help_text='Management Unit', limit_choices_to={'type': 4}, on_delete=django.db.models.deletion.PROTECT, related_name='curriculums', to='intranet_academic.ManagementUnit', verbose_name='Program Study'),
        ),
        migrations.CreateModel(
            name='CourseRequisite',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('score', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')], default='C', max_length=2, verbose_name='min graduated score')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requisites', to='intranet_academic.Course', verbose_name='course')),
                ('requisite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='required_by', to='intranet_academic.Course', verbose_name='requisite')),
            ],
            options={
                'verbose_name': 'Course prerequisite',
                'verbose_name_plural': 'Course prerequisite',
            },
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
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('code', models.CharField(editable=False, max_length=256, unique=True, verbose_name='code')),
                ('semester', models.PositiveIntegerField(choices=[(1, 'Odd'), (2, 'Even'), (3, 'Short')], default=1, verbose_name='semester')),
                ('date_start', models.DateField(help_text='Academic start date', null=True, verbose_name='date start')),
                ('date_registration', models.DateField(help_text='Registration open date', null=True, verbose_name='registration date')),
                ('date_preparation', models.DateField(help_text='Admin or staff preparing lecture and schedule.', null=True, verbose_name='preparation date')),
                ('date_lecture_open', models.DateField(help_text='Student start to learn.', null=True, verbose_name='lecture start date')),
                ('date_lecture_close', models.DateField(help_text='Lecture activity ended, teacher complete required report and score .', null=True, verbose_name='lecture end date')),
                ('date_completion', models.DateField(help_text='Lecture closed forever.', null=True, verbose_name='date completion')),
                ('date_end', models.DateField(help_text='Academic end', null=True, verbose_name='date end')),
                ('school_year', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='intranet_academic.SchoolYear', verbose_name='school year')),
            ],
            options={
                'verbose_name': 'academic year',
                'verbose_name_plural': 'academic years',
            },
        ),
        migrations.CreateModel(
            name='CourseEqualizer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('sks_old_course', models.IntegerField(verbose_name='SKS old')),
                ('sks_new_course', models.IntegerField(verbose_name='SKS new')),
                ('new_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='new_equalizers', to='intranet_academic.CurriculumCourse', verbose_name='New Course')),
                ('old_course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='old_equalizers', to='intranet_academic.CurriculumCourse', verbose_name='old course')),
            ],
            options={
                'verbose_name': 'course equalizer',
                'verbose_name_plural': 'course equalizers',
                'unique_together': {('old_course', 'new_course')},
            },
        ),
    ]
