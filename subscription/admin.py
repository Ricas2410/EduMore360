from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import SubscriptionPlan, Subscription, Payment, PaymentMethod


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan_type', 'billing_cycle', 'price', 'max_users', 'is_active')
    list_filter = ('plan_type', 'billing_cycle', 'is_active')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ('payment_date', 'status', 'amount', 'payment_method', 'transaction_id')
    can_delete = False
    max_num = 0


class SubscriptionDashboardLink(admin.ModelAdmin):
    """Empty model admin to add a link to the subscription dashboard in the admin sidebar."""

    def has_module_permission(self, _request):
        return True

    def has_permission(self, _request, _obj=None):
        return False

    def get_model_perms(self, _request):
        return {}


# We'll use a different approach to add the dashboard link


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan', 'status', 'start_date', 'end_date', 'auto_renew', 'is_group_admin', 'subscription_actions')
    list_filter = ('status', 'plan__plan_type', 'plan__billing_cycle', 'auto_renew', 'is_group_admin')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'subscription_actions')
    inlines = [PaymentInline]

    def subscription_actions(self, obj):
        """Add action buttons to the subscription list view."""
        dashboard_url = reverse('subscription:admin_subscription_dashboard')
        detail_url = reverse('subscription:admin_subscription_detail', args=[obj.id])

        return format_html(
            '<a href="{}" class="button" style="margin-right: 5px;">Dashboard</a>'
            '<a href="{}" class="button">Manage</a>',
            dashboard_url, detail_url
        )

    subscription_actions.short_description = 'Actions'

    fieldsets = (
        (None, {
            'fields': ('user', 'plan', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'canceled_at')
        }),
        ('Payment', {
            'fields': ('payment_method', 'auto_renew')
        }),
        ('Group', {
            'fields': ('is_group_admin', 'group')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('subscription', 'amount', 'status', 'payment_method', 'payment_date')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('subscription__user__email', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('subscription', 'amount', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'transaction_id', 'payment_date')
        }),
        ('Refund', {
            'fields': ('refund_date', 'refund_amount', 'refund_reason')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'brand', 'last4', 'is_default', 'is_active')
    list_filter = ('type', 'brand', 'is_default', 'is_active', 'payment_provider')
    search_fields = ('user__email', 'brand', 'last4', 'bank_name', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'type', 'is_default', 'is_active')
        }),
        ('Provider Details', {
            'fields': ('payment_provider', 'provider_payment_method_id')
        }),
        ('Card Details', {
            'fields': ('brand', 'last4', 'exp_month', 'exp_year'),
            'classes': ('collapse',),
        }),
        ('Bank Account Details', {
            'fields': ('bank_name', 'account_type'),
            'classes': ('collapse',),
        }),
        ('Mobile Money Details', {
            'fields': ('phone_number', 'mobile_provider'),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': ('metadata', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
