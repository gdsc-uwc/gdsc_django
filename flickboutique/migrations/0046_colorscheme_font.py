# Generated by Django 4.0.3 on 2022-03-30 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flickboutique', '0045_alter_businessinfo_colorscheme_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='colorscheme',
            name='font',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
