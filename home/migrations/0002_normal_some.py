# Generated by Django 3.2.9 on 2021-11-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='normal',
            name='some',
            field=models.TextField(blank=True, default=''),
        ),
    ]
