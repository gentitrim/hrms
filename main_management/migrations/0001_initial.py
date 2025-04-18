# Generated by Django 5.1.7 on 2025-04-05 12:40

import django.db.models.deletion
from django.conf import settings
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('address', models.CharField(blank=True, default='', max_length=250)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(blank=True, default='', max_length=14)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BranchManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('surname', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=128)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branch_manager', to='main_management.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
