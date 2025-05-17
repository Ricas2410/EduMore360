from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, Sum
from django.urls import reverse
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDay, TruncMonth

from .models import Subscription, Payment, SubscriptionPlan
from accounts.models import User

import csv
from datetime import datetime, timedelta
import json


@staff_member_required
def subscription_dashboard(request):
    """
    Admin dashboard for subscription management.
    """
    # Get subscription statistics
    total_subscriptions = Subscription.objects.count()
    active_subscriptions = Subscription.objects.filter(status='active').count()
    expired_subscriptions = Subscription.objects.filter(status='expired').count()
    canceled_subscriptions = Subscription.objects.filter(status='canceled').count()

    # Get revenue statistics
    total_revenue = Payment.objects.filter(status='completed').aggregate(Sum('amount'))['amount__sum'] or 0
    monthly_revenue = Payment.objects.filter(
        status='completed',
        payment_date__gte=timezone.now() - timedelta(days=30)
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # Get plan statistics
    plans = SubscriptionPlan.objects.annotate(
        subscribers=Count('subscriptions', filter=Q(subscriptions__status='active'))
    )

    # Get recent subscriptions
    recent_subscriptions = Subscription.objects.order_by('-created_at')[:10]

    # Get expiring soon subscriptions
    expiring_soon = Subscription.objects.filter(
        status='active',
        end_date__lte=timezone.now() + timedelta(days=7)
    ).order_by('end_date')[:10]

    # Get revenue over time (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    revenue_by_day = Payment.objects.filter(
        status='completed',
        payment_date__gte=thirty_days_ago
    ).annotate(
        day=TruncDay('payment_date')
    ).values('day').annotate(
        total=Sum('amount')
    ).order_by('day')

    # Format for chart
    revenue_dates = []
    revenue_amounts = []

    for entry in revenue_by_day:
        revenue_dates.append(entry['day'].strftime('%Y-%m-%d'))
        revenue_amounts.append(float(entry['total']))

    # Get subscriptions by plan type
    plan_type_data = Subscription.objects.filter(
        status='active'
    ).values(
        'plan__plan_type'
    ).annotate(
        count=Count('id')
    ).order_by('plan__plan_type')

    plan_types = []
    plan_counts = []

    for entry in plan_type_data:
        plan_type = entry['plan__plan_type']
        if plan_type == 'individual':
            plan_types.append('Individual')
        elif plan_type == 'family':
            plan_types.append('Family')
        elif plan_type == 'school':
            plan_types.append('School')
        else:
            plan_types.append(plan_type.capitalize())
        plan_counts.append(entry['count'])

    context = {
        'total_subscriptions': total_subscriptions,
        'active_subscriptions': active_subscriptions,
        'expired_subscriptions': expired_subscriptions,
        'canceled_subscriptions': canceled_subscriptions,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'plans': plans,
        'recent_subscriptions': recent_subscriptions,
        'expiring_soon': expiring_soon,
        'revenue_dates': json.dumps(revenue_dates),
        'revenue_amounts': json.dumps(revenue_amounts),
        'plan_types': json.dumps(plan_types),
        'plan_counts': json.dumps(plan_counts),
    }

    return render(request, 'admin/subscription/dashboard.html', context)


@staff_member_required
def subscription_list(request):
    """
    Admin view for listing all subscriptions with filtering and search.
    """
    subscriptions = Subscription.objects.all().select_related('user', 'plan')

    # Filter by status
    status = request.GET.get('status')
    if status:
        subscriptions = subscriptions.filter(status=status)

    # Filter by plan type
    plan_type = request.GET.get('plan_type')
    if plan_type:
        subscriptions = subscriptions.filter(plan__plan_type=plan_type)

    # Filter by billing cycle
    billing_cycle = request.GET.get('billing_cycle')
    if billing_cycle:
        subscriptions = subscriptions.filter(plan__billing_cycle=billing_cycle)

    # Filter by date range
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        start_date = parse_date(start_date)
        subscriptions = subscriptions.filter(start_date__gte=start_date)

    if end_date:
        end_date = parse_date(end_date)
        subscriptions = subscriptions.filter(end_date__lte=end_date)

    # Search by user
    search_query = request.GET.get('q')
    if search_query:
        subscriptions = subscriptions.filter(
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(subscriptions.order_by('-created_at'), 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Export as CSV if requested
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="subscriptions_{datetime.now().strftime("%Y%m%d")}.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'ID', 'User Email', 'User Name', 'Plan', 'Status',
            'Start Date', 'End Date', 'Auto Renew', 'Created At'
        ])

        for subscription in subscriptions:
            writer.writerow([
                subscription.id,
                subscription.user.email,
                subscription.user.get_full_name(),
                subscription.plan.name,
                subscription.status,
                subscription.start_date,
                subscription.end_date,
                'Yes' if subscription.auto_renew else 'No',
                subscription.created_at
            ])

        return response

    context = {
        'page_obj': page_obj,
        'status_choices': Subscription.STATUS_CHOICES,
        'plan_type_choices': SubscriptionPlan.PLAN_TYPE_CHOICES,
        'billing_cycle_choices': SubscriptionPlan.BILLING_CYCLE_CHOICES,
        'search_query': search_query,
        'status': status,
        'plan_type': plan_type,
        'billing_cycle': billing_cycle,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'admin/subscription/subscription_list.html', context)


@staff_member_required
def subscription_detail(request, subscription_id):
    """
    Admin view for viewing and managing a specific subscription.
    """
    subscription = get_object_or_404(Subscription, id=subscription_id)
    payments = Payment.objects.filter(subscription=subscription).order_by('-payment_date')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'cancel':
            subscription.status = 'canceled'
            subscription.canceled_at = timezone.now()
            subscription.auto_renew = False
            subscription.save()

            messages.success(request, f"Subscription for {subscription.user.email} has been canceled.")
            return redirect('subscription:admin_subscription_detail', subscription_id=subscription.id)

        elif action == 'activate':
            subscription.status = 'active'
            subscription.canceled_at = None
            subscription.save()

            messages.success(request, f"Subscription for {subscription.user.email} has been activated.")
            return redirect('subscription:admin_subscription_detail', subscription_id=subscription.id)

        elif action == 'extend':
            days = int(request.POST.get('days', 0))
            if days > 0:
                subscription.end_date = subscription.end_date + timedelta(days=days)
                subscription.save()

                messages.success(request, f"Subscription for {subscription.user.email} has been extended by {days} days.")
                return redirect('subscription:admin_subscription_detail', subscription_id=subscription.id)

    context = {
        'subscription': subscription,
        'payments': payments,
    }

    return render(request, 'admin/subscription/subscription_detail.html', context)
