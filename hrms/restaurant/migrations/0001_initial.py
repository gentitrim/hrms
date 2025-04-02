# Generated by Django 5.1.7 on 2025-04-01 23:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('branch_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.IntegerField()),
                ('status', models.CharField(choices=[('CONFIRMED', 'Confirmed'), ('CANCELED', 'Canceled')], default='CONFIRMED', max_length=128)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='branch_management.branchstaff')),
            ],
        ),
        migrations.CreateModel(
            name='Order_item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.IntegerField()),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurant.order')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch_management.products')),
            ],
        ),
    ]
