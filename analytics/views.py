from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Avg
from django.utils import timezone
from datetime import timedelta, date
from .models import PageView, QuizAnalytics, UserSession, DailyStats
from .utils import aggregate_daily_stats, get_country_flag_emoji


@staff_member_required
def analytics_dashboard(request):
    """Main analytics dashboard."""
    # Get date range (default: last 30 days)
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get or create today's stats
    today_stats = aggregate_daily_stats(end_date)
    
    # Get recent daily stats
    daily_stats = DailyStats.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Calculate totals for the period
    total_page_views = sum(stat.total_page_views for stat in daily_stats)
    total_unique_views = sum(stat.unique_page_views for stat in daily_stats)
    total_new_users = sum(stat.new_users for stat in daily_stats)
    total_quizzes_started = sum(stat.quizzes_started for stat in daily_stats)
    total_quizzes_completed = sum(stat.quizzes_completed for stat in daily_stats)
    
    # Calculate averages
    avg_daily_views = total_page_views / len(daily_stats) if daily_stats else 0
    completion_rate = (total_quizzes_completed / total_quizzes_started * 100) if total_quizzes_started > 0 else 0
    
    # Get top pages
    top_pages = (
        PageView.objects
        .filter(timestamp__date__gte=start_date)
        .values('path', 'page_title')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )
    
    # Get top countries (aggregate from daily stats)
    country_totals = {}
    for stat in daily_stats:
        for country, data in stat.top_countries.items():
            if country in country_totals:
                country_totals[country]['count'] += data['count']
            else:
                country_totals[country] = data.copy()
    
    # Sort countries by count
    top_countries = sorted(
        country_totals.items(),
        key=lambda x: x[1]['count'],
        reverse=True
    )[:10]
    
    # Get device type distribution
    device_stats = (
        PageView.objects
        .filter(timestamp__date__gte=start_date)
        .exclude(device_type='')
        .values('device_type')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    
    # Get browser distribution
    browser_stats = (
        PageView.objects
        .filter(timestamp__date__gte=start_date)
        .exclude(browser='')
        .values('browser')
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )
    
    # Prepare chart data
    chart_data = {
        'dates': [stat.date.strftime('%Y-%m-%d') for stat in daily_stats],
        'page_views': [stat.total_page_views for stat in daily_stats],
        'unique_views': [stat.unique_page_views for stat in daily_stats],
        'new_users': [stat.new_users for stat in daily_stats],
        'quizzes_started': [stat.quizzes_started for stat in daily_stats],
        'quizzes_completed': [stat.quizzes_completed for stat in daily_stats],
    }
    
    context = {
        'today_stats': today_stats,
        'total_page_views': total_page_views,
        'total_unique_views': total_unique_views,
        'total_new_users': total_new_users,
        'total_quizzes_started': total_quizzes_started,
        'total_quizzes_completed': total_quizzes_completed,
        'avg_daily_views': round(avg_daily_views, 1),
        'completion_rate': round(completion_rate, 1),
        'top_pages': top_pages,
        'top_countries': top_countries,
        'device_stats': device_stats,
        'browser_stats': browser_stats,
        'chart_data': chart_data,
        'date_range': f"{start_date} to {end_date}",
    }
    
    return render(request, 'analytics/dashboard.html', context)


@staff_member_required
def real_time_analytics(request):
    """Real-time analytics view."""
    # Get data from last 24 hours
    last_24h = timezone.now() - timedelta(hours=24)
    
    # Recent page views
    recent_views = (
        PageView.objects
        .filter(timestamp__gte=last_24h)
        .select_related('user')
        .order_by('-timestamp')[:50]
    )
    
    # Active sessions (last 30 minutes)
    active_threshold = timezone.now() - timedelta(minutes=30)
    active_sessions = (
        UserSession.objects
        .filter(last_activity__gte=active_threshold)
        .select_related('user')
        .order_by('-last_activity')
    )
    
    # Hourly breakdown for last 24 hours
    hourly_stats = []
    for i in range(24):
        hour_start = timezone.now() - timedelta(hours=i+1)
        hour_end = timezone.now() - timedelta(hours=i)
        
        hour_views = PageView.objects.filter(
            timestamp__gte=hour_start,
            timestamp__lt=hour_end
        ).count()
        
        hourly_stats.append({
            'hour': hour_start.strftime('%H:00'),
            'views': hour_views
        })
    
    hourly_stats.reverse()  # Show oldest to newest
    
    context = {
        'recent_views': recent_views,
        'active_sessions': active_sessions,
        'active_users_count': active_sessions.count(),
        'hourly_stats': hourly_stats,
    }
    
    return render(request, 'analytics/real_time.html', context)


@staff_member_required
def country_analytics(request):
    """Detailed country analytics."""
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get country statistics
    country_stats = (
        PageView.objects
        .filter(timestamp__date__gte=start_date)
        .exclude(country='')
        .values('country', 'country_code')
        .annotate(
            total_views=Count('id'),
            unique_visitors=Count('ip_address', distinct=True),
            registered_users=Count('user', distinct=True)
        )
        .order_by('-total_views')
    )
    
    # Add flags and calculate percentages
    total_views = sum(stat['total_views'] for stat in country_stats)
    
    enhanced_stats = []
    for stat in country_stats:
        stat['flag'] = get_country_flag_emoji(stat['country_code'])
        stat['percentage'] = round((stat['total_views'] / total_views * 100), 1) if total_views > 0 else 0
        enhanced_stats.append(stat)
    
    context = {
        'country_stats': enhanced_stats,
        'total_countries': len(enhanced_stats),
        'date_range': f"{start_date} to {end_date}",
    }
    
    return render(request, 'analytics/countries.html', context)
