# Generated by Django 3.2.5 on 2021-10-22 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_rename_queistion_paper_title_title_question_paper_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='title',
            old_name='remove_live',
            new_name='remove_live_minutes',
        ),
    ]
