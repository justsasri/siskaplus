# Generated by Django 3.0.6 on 2020-06-22 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intranet_lectures', '0004_auto_20200516_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='qrcode',
            field=models.ImageField(blank=True, editable=False, null=True, upload_to='qrcode'),
        ),
    ]
