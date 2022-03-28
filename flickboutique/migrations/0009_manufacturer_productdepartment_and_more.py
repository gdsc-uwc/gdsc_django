# Generated by Django 4.0.3 on 2022-03-17 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flickboutique', '0008_remove_businessinfo_username_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturerName', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ProductDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departmentName', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='businessinfo',
            name='businessName',
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=128)),
                ('productPrice', models.IntegerField()),
                ('productInformation', models.CharField(max_length=2048)),
                ('productRating', models.IntegerField()),
                ('productDepartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_department', to='flickboutique.productdepartment')),
                ('productManufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_manufacturer', to='flickboutique.manufacturer')),
            ],
        ),
    ]
