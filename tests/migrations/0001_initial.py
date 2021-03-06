# Generated by Django 3.2.5 on 2021-10-19 10:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Queistion_Paper_Title', models.CharField(max_length=200)),
                ('exam_type', models.CharField(blank=True, choices=[('Jee', 'Jee'), ('Neet', 'Neet')], default='Jee', max_length=100)),
                ('marking_scheme', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='0', help_text='assigned marks for every questions', max_length=200)),
                ('minus_marking_scheme', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')], default='0', max_length=200)),
                ('scheduled_time', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('is_live', models.BooleanField(default=False)),
                ('end_hours', models.FloatField(default=1)),
                ('description', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts', models.IntegerField(blank=True, default=0)),
                ('marks', models.IntegerField(blank=True, default=0)),
                ('rank', models.IntegerField(blank=True, default=0)),
                ('exam_data', models.TextField(blank=True, default='None')),
                ('want_try_again', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(blank=True, default=0)),
                ('paper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Physics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q_No', models.IntegerField(default=0, help_text='increament every time for unique paper type')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('single', 'single'), ('write', 'write'), ('multiselect', 'multiselect')], default='single', help_text='Please enter your answerin option1 for write type questions', max_length=20)),
                ('option1', models.CharField(blank=True, max_length=500)),
                ('option2', models.CharField(blank=True, max_length=500)),
                ('option3', models.CharField(blank=True, max_length=500)),
                ('option4', models.CharField(blank=True, max_length=500)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=100)),
                ('explanation', models.TextField(blank=True, default='None')),
                ('paper_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Math',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q_No', models.IntegerField(default=0, help_text='increament every time for unique paper type')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('single', 'single'), ('write', 'write'), ('multiselect', 'multiselect')], default='single', help_text='Please enter your answerin option1 for write type questions', max_length=20)),
                ('option1', models.CharField(blank=True, max_length=500)),
                ('option2', models.CharField(blank=True, max_length=500)),
                ('option3', models.CharField(blank=True, max_length=500)),
                ('option4', models.CharField(blank=True, max_length=500)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=100)),
                ('explanation', models.TextField(blank=True, default='None')),
                ('paper_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chemistry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q_No', models.IntegerField(default=0, help_text='increament every time for unique paper type')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('single', 'single'), ('write', 'write'), ('multiselect', 'multiselect')], default='single', help_text='Please enter your answerin option1 for write type questions', max_length=20)),
                ('option1', models.CharField(blank=True, max_length=500)),
                ('option2', models.CharField(blank=True, max_length=500)),
                ('option3', models.CharField(blank=True, max_length=500)),
                ('option4', models.CharField(blank=True, max_length=500)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=100)),
                ('explanation', models.TextField(blank=True, default='None')),
                ('paper_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Biology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q_No', models.IntegerField(default=0, help_text='increament every time for unique paper type')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('single', 'single'), ('write', 'write'), ('multiselect', 'multiselect')], default='single', help_text='Please enter your answerin option1 for write type questions', max_length=20)),
                ('option1', models.CharField(blank=True, max_length=500)),
                ('option2', models.CharField(blank=True, max_length=500)),
                ('option3', models.CharField(blank=True, max_length=500)),
                ('option4', models.CharField(blank=True, max_length=500)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=100)),
                ('explanation', models.TextField(blank=True, default='None')),
                ('paper_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agriculture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Q_No', models.IntegerField(default=0, help_text='increament every time for unique paper type')),
                ('description', models.TextField()),
                ('type', models.CharField(choices=[('single', 'single'), ('write', 'write'), ('multiselect', 'multiselect')], default='single', help_text='Please enter your answerin option1 for write type questions', max_length=20)),
                ('option1', models.CharField(blank=True, max_length=500)),
                ('option2', models.CharField(blank=True, max_length=500)),
                ('option3', models.CharField(blank=True, max_length=500)),
                ('option4', models.CharField(blank=True, max_length=500)),
                ('difficulty', models.CharField(blank=True, choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], default='A', max_length=100)),
                ('explanation', models.TextField(blank=True, default='None')),
                ('paper_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.title')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
