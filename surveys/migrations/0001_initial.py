# Generated by Django 5.2.3 on 2025-06-21 03:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammerResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('years', models.CharField(max_length=10)),
                ('primary_language', models.CharField(blank=True, max_length=100)),
                ('languages', models.JSONField(blank=True, default=list)),
                ('other_language', models.CharField(blank=True, max_length=100)),
                ('algorithms', models.CharField(max_length=50)),
                ('data_structures', models.CharField(max_length=50)),
                ('challenges', models.CharField(max_length=50)),
                ('git', models.CharField(max_length=50)),
                ('ci_cd', models.CharField(max_length=50)),
                ('testing', models.CharField(max_length=50)),
                ('open_source', models.CharField(max_length=50)),
                ('largest_project', models.TextField(blank=True)),
                ('agile', models.CharField(max_length=50)),
                ('architecture', models.CharField(max_length=50)),
                ('concepts', models.CharField(max_length=50)),
                ('deployment', models.CharField(max_length=50)),
                ('platforms', models.JSONField(blank=True, default=list)),
                ('platform_other', models.CharField(blank=True, max_length=100)),
                ('interests', models.JSONField(blank=True, default=list)),
                ('interests_other', models.CharField(blank=True, max_length=100)),
                ('learning', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('section', models.CharField(blank=True, max_length=200)),
                ('input_type', models.CharField(choices=[('short_text', 'Short Text'), ('long_text', 'Long Text'), ('select', 'Select'), ('checkbox_multiple', 'Checkboxes'), ('number', 'Number')], default='short_text', max_length=30)),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(max_length=64)),
                ('age', models.CharField(choices=[('0–2', '0–2 (Infant)'), ('3–12', '3–12 (Child)'), ('13–17', '13–17 (Teen)'), ('18–24', '18–24 (Young Adult)'), ('25–34', '25–34 (Early Adult)'), ('35–44', '35–44 (Middle Adult)'), ('45–54', '45–54 (Older Adult)'), ('55–64', '55–64 (Senior)'), ('65+', '65+ (Elder)')], max_length=16)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('total_score', models.FloatField()),
                ('scores', models.JSONField()),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.questionnaire')),
            ],
        ),
        migrations.CreateModel(
            name='SectionPoll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.question')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.section')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('section', 'poll')},
            },
        ),
        migrations.AddField(
            model_name='section',
            name='polls',
            field=models.ManyToManyField(blank=True, related_name='sections', through='surveys.SectionPoll', to='polls.question'),
        ),
        migrations.CreateModel(
            name='SurveySection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(default=0)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.section')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveys.survey')),
            ],
            options={
                'ordering': ['order'],
                'unique_together': {('survey', 'section')},
            },
        ),
        migrations.AddField(
            model_name='survey',
            name='sections',
            field=models.ManyToManyField(related_name='surveys', through='surveys.SurveySection', to='surveys.section'),
        ),
    ]
