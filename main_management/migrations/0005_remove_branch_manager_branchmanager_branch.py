# Generated by Django 5.1.7 on 2025-04-06 12:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_management', '0004_remove_branchmanager_branch_branch_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branch',
            name='manager',
        ),
        migrations.AddField(
            model_name='branchmanager',
            name='branch',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='branch_manager', to='main_management.branch'),
            preserve_default=False,
        ),
    ]
