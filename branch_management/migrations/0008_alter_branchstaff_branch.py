# Generated by Django 5.1.7 on 2025-04-13 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branch_management', '0007_merge_20250412_1537'),
        ('main_management', '0007_remove_branchmanager_user_branchmanager_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branchstaff',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_management.branch'),
        ),
    ]
