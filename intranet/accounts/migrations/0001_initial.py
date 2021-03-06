# Generated by Django 3.0.6 on 2020-05-08 12:30

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('show_title', models.BooleanField(default=False, help_text='Show Mr or Mrs in front of name', verbose_name='show title')),
                ('show_academic_title', models.BooleanField(default=False, help_text='Show name with academic title', verbose_name='Show academic title')),
                ('title', models.CharField(blank=True, max_length=256, null=True, verbose_name='title')),
                ('front_title', models.CharField(blank=True, help_text='Front academic title.', max_length=256, null=True, verbose_name='front title')),
                ('back_title', models.CharField(blank=True, help_text='Back academic title.', max_length=256, null=True, verbose_name='back title')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='uuid')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('first_name', models.CharField(max_length=30, verbose_name='full name')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_student', models.BooleanField(default=False, help_text='Designates whether the user is a student.', verbose_name='student')),
                ('is_teacher', models.BooleanField(default=False, help_text='Designates whether the user is a teacher.', verbose_name='teacher')),
                ('is_employee', models.BooleanField(default=False, help_text='Designates whether the user is a employee.', verbose_name='employee')),
                ('is_management', models.BooleanField(default=False, help_text='Designates whether the user is a management.', verbose_name='management')),
                ('is_matriculant', models.BooleanField(default=False, help_text='Designates whether the user is a matriculant or student candidate.', verbose_name='matriculant')),
                ('is_applicant', models.BooleanField(default=False, help_text='Designates whether the user is a employee or teacher applicant.', verbose_name='applicant')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
