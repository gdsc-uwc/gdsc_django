# Generated by Django 4.0.3 on 2022-03-28 01:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flickboutique', '0039_remove_product_soldby_product_soldby'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_checker', to=settings.AUTH_USER_MODEL)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_maker', to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(related_name='ordered_items', to='flickboutique.cartitem')),
            ],
        ),
    ]
