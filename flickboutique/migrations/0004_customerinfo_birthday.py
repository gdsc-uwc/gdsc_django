# Generated by Django 4.0.3 on 2022-03-16 22:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('flickboutique', '0003_rename_business_businessinfo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerinfo',
            name='birthday',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
