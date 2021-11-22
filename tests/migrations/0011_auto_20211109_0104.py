# Generated by Django 3.2 on 2021-11-08 19:34

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0010_alter_title_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agriculture',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='agriculture',
            name='explanation',
            field=tinymce.models.HTMLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='biology',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='biology',
            name='explanation',
            field=tinymce.models.HTMLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='chemistry',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='chemistry',
            name='explanation',
            field=tinymce.models.HTMLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='math',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='math',
            name='explanation',
            field=tinymce.models.HTMLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='physics',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
        migrations.AlterField(
            model_name='physics',
            name='explanation',
            field=tinymce.models.HTMLField(blank=True, default='None'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=tinymce.models.HTMLField(blank=True, default=''),
        ),
    ]
