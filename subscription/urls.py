from django.urls import path
from . import views
from . import admin_views

app_name = 'subscription'

urlpatterns = [
    # Subscription plans
    path('', views.subscription_plans, name='subscription_plans'),
    path('subscribe/<str:plan_type>/<str:billing_cycle>/', views.subscribe, name='subscribe'),
    path('access-denied/', views.access_denied, name='access_denied'),

    # Plan management
    path('change-plan/', views.change_plan, name='change_plan'),
    path('cancel-scheduled-change/<int:subscription_id>/', views.cancel_scheduled_change, name='cancel_scheduled_change'),
    path('toggle-auto-renew/<int:subscription_id>/', views.toggle_auto_renew, name='toggle_auto_renew'),

    # Payment processing
    path('payment/<int:subscription_id>/', views.payment, name='payment'),
    path('payment/success/<int:subscription_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:subscription_id>/', views.payment_cancel, name='payment_cancel'),
    path('payment/webhook/', views.payment_webhook, name='payment_webhook'),
    path('payment/process/<int:subscription_id>/', views.process_payment, name='process_payment'),
    path('payment/paystack/<int:subscription_id>/', views.process_paystack_payment, name='process_paystack_payment'),
    path('payment/mobile-money/<int:subscription_id>/', views.process_mobile_money, name='process_mobile_money'),
    path('payment/bank-transfer/<int:subscription_id>/', views.process_bank_transfer, name='process_bank_transfer'),

    # Subscription management
    path('manage/', views.manage_subscription, name='manage_subscription'),
    path('cancel/<int:subscription_id>/', views.cancel_subscription, name='cancel_subscription'),
    path('toggle-auto-renew/<int:subscription_id>/', views.toggle_auto_renew, name='toggle_auto_renew'),

    # Payment method management
    path('payment-methods/add/', views.add_payment_method, name='add_payment_method'),
    path('payment-methods/remove/<str:payment_method_id>/', views.remove_payment_method, name='remove_payment_method'),
    path('payment-methods/set-default/<str:payment_method_id>/', views.set_default_payment_method, name='set_default_payment_method'),

    # Family/Enterprise subscription management
    path('group/members/', views.group_members, name='group_members'),
    path('group/add-member/', views.add_group_member, name='add_group_member'),
    path('group/remove-member/<int:user_id>/', views.remove_group_member, name='remove_group_member'),

    # Payment history
    path('payments/', views.payment_history, name='payment_history'),
    path('invoice/<int:payment_id>/', views.invoice, name='invoice'),

    # Admin views
    path('admin/dashboard/', admin_views.subscription_dashboard, name='admin_subscription_dashboard'),
    path('admin/subscriptions/', admin_views.subscription_list, name='admin_subscription_list'),
    path('admin/subscriptions/<int:subscription_id>/', admin_views.subscription_detail, name='admin_subscription_detail'),
]
