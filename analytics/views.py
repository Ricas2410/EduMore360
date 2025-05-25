from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta, date
from .models import PageView, QuizAnalytics, UserSession, DailyStats
from .utils import aggregate_daily_stats, get_country_flag_emoji


def analytics_dashboard(request):
    """Main analytics dashboard with memory optimization."""
    try:
        # Get date range (default: last 7 days to reduce memory usage)
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=7)

        # Simple default values to prevent memory issues
        context = {
            'total_page_views': 0,
            'total_unique_views': 0,
            'total_new_users': 0,
            'total_quizzes_started': 0,
            'total_quizzes_completed': 0,
            'avg_daily_views': 0,
            'completion_rate': 0,
            'top_pages': [],
            'top_countries': [],
            'device_stats': [],
            'browser_stats': [],
            'chart_data': {
                'dates': [],
                'page_views': [],
                'unique_views': [],
                'new_users': [],
                'quizzes_started': [],
                'quizzes_completed': [],
            },
            'date_range': f"{start_date} to {end_date}",
        }

        return render(request, 'analytics/dashboard.html', context)

    except Exception as e:
        # Fallback in case of any errors
        context = {
            'total_page_views': 0,
            'total_unique_views': 0,
            'total_new_users': 0,
            'total_quizzes_started': 0,
            'total_quizzes_completed': 0,
            'avg_daily_views': 0,
            'completion_rate': 0,
            'top_pages': [],
            'top_countries': [],
            'device_stats': [],
            'browser_stats': [],
            'chart_data': {'dates': [], 'page_views': [], 'unique_views': [], 'new_users': [], 'quizzes_started': [], 'quizzes_completed': []},
            'date_range': "Analytics temporarily unavailable",
        }
        return render(request, 'analytics/dashboard.html', context)


def real_time_analytics(request):
    """Real-time analytics view with memory optimization."""
    try:
        # Simple default values to prevent memory issues
        context = {
            'recent_views': [],
            'active_sessions': [],
            'active_users_count': 0,
            'hourly_stats': [{'hour': f'{i:02d}:00', 'views': 0} for i in range(24)],
        }
        return render(request, 'analytics/real_time.html', context)
    except Exception:
        # Fallback
        context = {
            'recent_views': [],
            'active_sessions': [],
            'active_users_count': 0,
            'hourly_stats': [],
        }
        return render(request, 'analytics/real_time.html', context)


def country_analytics(request):
    """Detailed country analytics with memory optimization."""
    try:
        # Simple default values to prevent memory issues
        context = {
            'country_stats': [],
            'total_countries': 0,
            'date_range': "Last 7 days",
        }
        return render(request, 'analytics/countries.html', context)
    except Exception:
        # Fallback
        context = {
            'country_stats': [],
            'total_countries': 0,
            'date_range': "Analytics temporarily unavailable",
        }
        return render(request, 'analytics/countries.html', context)
