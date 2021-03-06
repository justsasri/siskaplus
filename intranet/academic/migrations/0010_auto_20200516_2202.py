# Generated by Django 3.0.6 on 2020-05-16 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet_academic', '0009_auto_20200516_2132'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conversionstudentscore',
            old_name='ori_alphabetic_score',
            new_name='ori_alphabetic',
        ),
        migrations.RenameField(
            model_name='conversionstudentscore',
            old_name='ori_numeric_score',
            new_name='ori_numeric',
        ),
        migrations.AddField(
            model_name='conversionstudentscore',
            name='reference',
            field=models.CharField(default=1, max_length=256, verbose_name='reference'),
            preserve_default=False,
        ),
    ]
