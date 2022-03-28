# Generated by Django 4.0.3 on 2022-03-28 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flickboutique', '0038_alter_customershoppingcart_items'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='soldBy',
        ),
        migrations.AddField(
            model_name='product',
            name='soldBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_seller', to=settings.AUTH_USER_MODEL),
        ),
    ]
