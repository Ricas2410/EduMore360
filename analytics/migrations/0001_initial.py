# Generated by Django 5.0.6 on 2025-05-25 08:26

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quiz', '0006_quiz_is_featured'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('total_users', models.PositiveIntegerField(default=0)),
                ('new_users', models.PositiveIntegerField(default=0)),
                ('active_users', models.PositiveIntegerField(default=0)),
                ('total_page_views', models.PositiveIntegerField(default=0)),
                ('unique_page_views', models.PositiveIntegerField(default=0)),
                ('quizzes_started', models.PositiveIntegerField(default=0)),
                ('quizzes_completed', models.PositiveIntegerField(default=0)),
                ('average_score', models.FloatField(blank=True, null=True)),
                ('top_countries', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'analytics_daily_stats',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('path', models.CharField(max_length=500)),
                ('page_title', models.CharField(blank=True, max_length=200)),
                ('referrer', models.URLField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('country_code', models.CharField(blank=True, max_length=2)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('region', models.CharField(blank=True, max_length=100)),
                ('device_type', models.CharField(blank=True, max_length=20)),
                ('browser', models.CharField(blank=True, max_length=50)),
                ('operating_system', models.CharField(blank=True, max_length=50)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('time_on_page', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'analytics_pageview',
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['timestamp'], name='analytics_p_timesta_835321_idx'), models.Index(fields=['user'], name='analytics_p_user_id_23554e_idx'), models.Index(fields=['path'], name='analytics_p_path_3382b5_idx'), models.Index(fields=['country'], name='analytics_p_country_59a416_idx'), models.Index(fields=['ip_address'], name='analytics_p_ip_addr_3b1d53_idx')],
            },
        ),
        migrations.CreateModel(
            name='QuizAnalytics',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('total_questions', models.PositiveIntegerField()),
                ('correct_answers', models.PositiveIntegerField(default=0)),
                ('ip_address', models.GenericIPAddressField()),
                ('country', models.CharField(blank=True, max_length=100)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.quiz')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'analytics_quiz',
                'ordering': ['-started_at'],
                'indexes': [models.Index(fields=['started_at'], name='analytics_q_started_aacb5b_idx'), models.Index(fields=['quiz'], name='analytics_q_quiz_id_1c8bb4_idx'), models.Index(fields=['user'], name='analytics_q_user_id_d10414_idx')],
            },
        ),
        migrations.CreateModel(
            name='UserSession',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('session_key', models.CharField(max_length=40, unique=True)),
                ('started_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_activity', models.DateTimeField(default=django.utils.timezone.now)),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('page_views', models.PositiveIntegerField(default=0)),
                ('duration', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'analytics_session',
                'ordering': ['-started_at'],
                'indexes': [models.Index(fields=['started_at'], name='analytics_s_started_0e04d8_idx'), models.Index(fields=['user'], name='analytics_s_user_id_397035_idx'), models.Index(fields=['session_key'], name='analytics_s_session_dad159_idx')],
            },
        ),
    ]
