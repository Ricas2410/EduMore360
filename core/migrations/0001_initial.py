# Generated by Django 5.0.6 on 2025-05-11 22:50

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('curriculum', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HeroSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, max_length=300)),
                ('description', models.TextField(blank=True)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='hero_backgrounds/')),
                ('foreground_image', models.ImageField(blank=True, null=True, upload_to='hero_foregrounds/')),
                ('mascot_image', models.ImageField(blank=True, null=True, upload_to='mascots/')),
                ('mascot_name', models.CharField(blank=True, max_length=50)),
                ('cta_text', models.CharField(blank=True, help_text='Call to action button text', max_length=50)),
                ('cta_url', models.CharField(blank=True, help_text='URL for the call to action button', max_length=200)),
                ('position', models.CharField(choices=[('home', 'Home Page'), ('dashboard', 'Student Dashboard'), ('subscription', 'Subscription Page'), ('curriculum', 'Curriculum Page'), ('quiz', 'Quiz Page')], default='home', max_length=20)),
                ('target_audience', models.CharField(choices=[('all', 'All Users'), ('elementary', 'Elementary School (Grades 1-5)'), ('middle', 'Middle School (Grades 6-8)'), ('high', 'High School (Grades 9-12)'), ('parents', 'Parents'), ('teachers', 'Teachers')], default='all', max_length=20)),
                ('animation_enabled', models.BooleanField(default=True)),
                ('use_bright_colors', models.BooleanField(default=True, help_text='Use bright, kid-friendly colors')),
                ('is_active', models.BooleanField(default=True)),
                ('display_order', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Hero Section',
                'verbose_name_plural': 'Hero Sections',
                'ordering': ['position', 'display_order'],
            },
        ),
        migrations.CreateModel(
            name='KidFriendlyTheme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('theme_type', models.CharField(choices=[('default', 'Default Theme'), ('space', 'Space Adventure'), ('ocean', 'Ocean Explorer'), ('jungle', 'Jungle Safari'), ('dinosaur', 'Dinosaur World'), ('fantasy', 'Fantasy Kingdom'), ('science', 'Science Lab')], default='default', max_length=20)),
                ('primary_color', models.CharField(default='#4A6FFF', max_length=20)),
                ('secondary_color', models.CharField(default='#FF6B6B', max_length=20)),
                ('accent_color', models.CharField(default='#FFD166', max_length=20)),
                ('background_image', models.ImageField(blank=True, null=True, upload_to='theme_backgrounds/')),
                ('header_image', models.ImageField(blank=True, null=True, upload_to='theme_headers/')),
                ('footer_image', models.ImageField(blank=True, null=True, upload_to='theme_footers/')),
                ('mascot_image', models.ImageField(blank=True, null=True, upload_to='theme_mascots/')),
                ('mascot_name', models.CharField(blank=True, max_length=50)),
                ('use_rounded_corners', models.BooleanField(default=True)),
                ('use_animations', models.BooleanField(default=True)),
                ('use_sound_effects', models.BooleanField(default=False)),
                ('min_grade', models.PositiveIntegerField(default=1)),
                ('max_grade', models.PositiveIntegerField(default=12)),
                ('is_active', models.BooleanField(default=True)),
                ('is_default', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Kid-Friendly Theme',
                'verbose_name_plural': 'Kid-Friendly Themes',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_percentage', models.PositiveIntegerField(default=0)),
                ('last_activity', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-last_activity'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('notification_type', models.CharField(choices=[('info', 'Information'), ('success', 'Success'), ('warning', 'Warning'), ('error', 'Error')], default='info', max_length=10)),
                ('category', models.CharField(choices=[('system', 'System'), ('subscription', 'Subscription'), ('content', 'Content'), ('quiz', 'Quiz'), ('account', 'Account')], default='system', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('url', models.CharField(blank=True, help_text='URL to redirect to when notification is clicked', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='NotificationPreferences',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications', models.BooleanField(default=True, help_text='Receive notifications via email')),
                ('quiz_reminders', models.BooleanField(default=True, help_text='Receive reminders for incomplete quizzes')),
                ('new_content_notifications', models.BooleanField(default=True, help_text='Receive notifications when new content is added')),
                ('achievement_notifications', models.BooleanField(default=True, help_text='Receive notifications when you earn new achievements')),
                ('subscription_notifications', models.BooleanField(default=True, help_text='Receive notifications about your subscription status')),
                ('push_notifications', models.BooleanField(default=True, help_text='Receive push notifications on mobile devices')),
                ('notification_frequency', models.CharField(choices=[('immediate', 'Immediate'), ('daily', 'Daily Digest'), ('weekly', 'Weekly Digest')], default='immediate', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='notification_preferences', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Notification Preferences',
                'verbose_name_plural': 'Notification Preferences',
            },
        ),
        migrations.CreateModel(
            name='SystemConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='EduMore360', max_length=100)),
                ('site_description', models.TextField(blank=True)),
                ('maintenance_mode', models.BooleanField(default=False)),
                ('smtp_host', models.CharField(default='smtp.gmail.com', max_length=100)),
                ('smtp_port', models.PositiveIntegerField(default=587)),
                ('smtp_use_tls', models.BooleanField(default=True)),
                ('smtp_username', models.CharField(default='skillnetservices@gmail.com', max_length=100)),
                ('smtp_password', models.CharField(default='tdms ckdk tmgo fado', max_length=100)),
                ('default_from_email', models.EmailField(default='skillnetservices@gmail.com', max_length=254)),
                ('enforce_single_session', models.BooleanField(default=False, help_text='If enabled, users can only be logged in from one device at a time')),
                ('session_timeout_minutes', models.PositiveIntegerField(default=30, help_text='Session timeout in minutes')),
                ('allow_registration', models.BooleanField(default=True)),
                ('require_email_verification', models.BooleanField(default=True)),
                ('enable_google_login', models.BooleanField(default=True)),
                ('paystack_secret_key', models.CharField(blank=True, max_length=100)),
                ('paystack_public_key', models.CharField(blank=True, max_length=100)),
                ('currency', models.CharField(default='USD', max_length=3)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='system_config_updates', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'System Configuration',
                'verbose_name_plural': 'System Configuration',
            },
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('achievement_type', models.CharField(choices=[('completion', 'Content Completion'), ('quiz', 'Quiz Performance'), ('streak', 'Learning Streak'), ('milestone', 'Learning Milestone')], max_length=20)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='achievement_icons/')),
                ('points', models.PositiveIntegerField(default=0)),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
                ('class_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='curriculum.classlevel')),
                ('curriculum', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='curriculum.curriculum')),
            ],
            options={
                'ordering': ['-earned_at'],
            },
        ),
    ]
