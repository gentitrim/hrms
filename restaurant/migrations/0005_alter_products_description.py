# Generated by Django 5.1.5 on 2025-03-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0004_products_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='description',
            field=models.CharField(blank=True, default=None, max_length=250),
        ),
    ]
