# Generated by Django 5.1.3 on 2025-07-21 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultant', '0002_remove_consultantprofile_experience_years'),
    ]

    operations = [
        migrations.RenameField(
            model_name='availabletime',
            old_name='end_time',
            new_name='endTime',
        ),
        migrations.RenameField(
            model_name='availabletime',
            old_name='is_active',
            new_name='isActive',
        ),
        migrations.RenameField(
            model_name='availabletime',
            old_name='start_time',
            new_name='startTime',
        ),
        migrations.RenameField(
            model_name='consultantprofile',
            old_name='full_name',
            new_name='fullName',
        ),
        migrations.RenameField(
            model_name='consultantprofile',
            old_name='is_active',
            new_name='isActive',
        ),
    ]
