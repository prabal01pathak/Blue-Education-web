# Generated by Django 3.2.5 on 2021-10-10 14:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0007_auto_20211010_1557'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentdata',
            name='answers',
        ),
        migrations.AddField(
            model_name='studentdata',
            name='chemistry_answers',
            field=models.TextField(blank=True, default='None'),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='chemistry_score',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='math_answers',
            field=models.TextField(blank=True, default='None'),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='math_score',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='physics_answers',
            field=models.TextField(blank=True, default='None'),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='physics_score',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='studentdata',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentdata',
            name='want_try_again',
            field=models.BooleanField(default=False),
        ),
    ]
