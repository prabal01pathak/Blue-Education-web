# Generated by Django 3.2.5 on 2021-10-10 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0008_auto_20211010_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='submitted_at',
            field=models.DateTimeField(default=0),
        ),
    ]
