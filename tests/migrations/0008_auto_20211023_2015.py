# Generated by Django 3.2.5 on 2021-10-23 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_auto_20211023_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agriculture',
            name='marking',
            field=models.FloatField(blank=True, default=0, help_text='assigned marks for this questions if same as title leave it.'),
        ),
        migrations.AlterField(
            model_name='biology',
            name='marking',
            field=models.FloatField(blank=True, default=0, help_text='assigned marks for this questions if same as title leave it.'),
        ),
        migrations.AlterField(
            model_name='chemistry',
            name='marking',
            field=models.FloatField(blank=True, default=0, help_text='assigned marks for this questions if same as title leave it.'),
        ),
        migrations.AlterField(
            model_name='math',
            name='marking',
            field=models.FloatField(blank=True, default=0, help_text='assigned marks for this questions if same as title leave it.'),
        ),
        migrations.AlterField(
            model_name='physics',
            name='marking',
            field=models.FloatField(blank=True, default=0, help_text='assigned marks for this questions if same as title leave it.'),
        ),
    ]
