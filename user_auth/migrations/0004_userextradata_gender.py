# Generated by Django 3.2.5 on 2021-10-19 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_userextradata'),
    ]

    operations = [
        migrations.AddField(
            model_name='userextradata',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=10),
        ),
    ]
