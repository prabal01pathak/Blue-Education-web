# Generated by Django 3.2.9 on 2021-11-23 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JEE', '0012_auto_20211119_1719'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='some',
            field=models.TextField(blank=True, default=''),
        ),
    ]
