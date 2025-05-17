from django.db import models
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    """Model representing a subscription plan."""

    PLAN_TYPE_CHOICES = (
        ('free', 'Free Tier'),
        ('tier_one', 'Tier One'),
        ('tier_two', 'Tier Two'),
        ('tier_three', 'Tier Three'),
    )

    BILLING_CYCLE_CHOICES = (
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    )

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle = models.CharField(max_length=10, choices=BILLING_CYCLE_CHOICES)
    yearly_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text="Discount percentage for yearly subscriptions")
    features = models.TextField(help_text="Features included in this plan, one per line")
    max_users = models.PositiveIntegerField(default=1, help_text="Maximum number of users allowed (for Family/Enterprise plans)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Access control fields
    all_curriculums = models.BooleanField(default=False, help_text="If True, this plan has access to all curriculums")
    all_grade_levels = models.BooleanField(default=False, help_text="If True, this plan has access to all grade levels within the allowed curriculums")

    class Meta:
        ordering = ['price']
        unique_together = ['plan_type', 'billing_cycle']

    def __str__(self):
        return f"{self.name} ({self.get_billing_cycle_display()})"

    @property
    def monthly_price(self):
        """Calculate the monthly price."""
        if self.billing_cycle == 'monthly':
            return self.price
        # Yearly price divided by 12
        return round(self.price / 12, 2)

    @property
    def yearly_price(self):
        """Calculate the yearly price."""
        if self.billing_cycle == 'yearly':
            return self.price
        # Monthly price multiplied by 12 with discount applied
        monthly_total = self.price * 12
        discount_amount = monthly_total * (self.yearly_discount_percentage / 100)
        return round(monthly_total - discount_amount, 2)

    @property
    def yearly_savings(self):
        """Calculate savings for yearly subscription compared to monthly."""
        if self.billing_cycle == 'yearly':
            monthly_plan = SubscriptionPlan.objects.filter(
                plan_type=self.plan_type,
                billing_cycle='monthly'
            ).first()

            if monthly_plan:
                # Calculate the full yearly price without discount
                full_yearly_price = monthly_plan.price * 12
                # Return the difference between full price and discounted price
                return round(full_yearly_price - self.price, 2)

        return 0

    @property
    def yearly_savings_percentage(self):
        """Calculate percentage savings for yearly subscription compared to monthly."""
        if self.billing_cycle == 'yearly':
            monthly_plan = SubscriptionPlan.objects.filter(
                plan_type=self.plan_type,
                billing_cycle='monthly'
            ).first()

            if monthly_plan:
                full_yearly_price = monthly_plan.price * 12
                if full_yearly_price > 0:
                    return round((self.yearly_savings / full_yearly_price) * 100, 2)

        return 0

    @property
    def features_list(self):
        """Parse the features text into a list of features."""
        if not self.features:
            return []

        # Split by newline and remove empty lines and leading/trailing whitespace
        features = [f.strip() for f in self.features.split('\n') if f.strip()]

        # Remove leading dash or bullet if present
        features = [f[1:].strip() if f.startswith('-') or f.startswith('•') else f for f in features]

        return features


class Subscription(models.Model):
    """Model representing a user's subscription."""

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Dates
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    canceled_at = models.DateTimeField(null=True, blank=True)

    # Payment details
    payment_method = models.CharField(max_length=100, blank=True)
    auto_renew = models.BooleanField(default=True)

    # For family/enterprise plans
    is_group_admin = models.BooleanField(default=False)
    group = models.ForeignKey('accounts.UserGroup', on_delete=models.SET_NULL, null=True, blank=True, related_name='subscriptions')

    # For scheduled plan changes
    scheduled_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='scheduled_subscriptions')
    scheduled_change_type = models.CharField(max_length=20, choices=(
        ('upgrade', 'Upgrade'),
        ('downgrade', 'Downgrade'),
        ('change_billing', 'Change Billing Cycle')
    ), null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"

    @property
    def is_active(self):
        """Check if the subscription is active."""
        return (
            self.status == 'active' and
            self.start_date <= timezone.now() and
            self.end_date > timezone.now()
        )

    @property
    def days_remaining(self):
        """Calculate the number of days remaining in the subscription."""
        if not self.is_active:
            return 0

        delta = self.end_date - timezone.now()
        return max(0, delta.days)

    def has_access_to_curriculum(self, curriculum):
        """Check if the subscription has access to a specific curriculum."""
        if not self.is_active:
            return False

        # If the plan allows all curriculums, return True
        if self.plan.all_curriculums:
            return True

        # Check if there's a specific access for this curriculum
        return self.curriculum_accesses.filter(curriculum=curriculum).exists()

    def has_access_to_class_level(self, curriculum, class_level):
        """Check if the subscription has access to a specific class level within a curriculum."""
        if not self.is_active:
            return False

        # If the plan doesn't allow access to the curriculum, return False
        if not self.has_access_to_curriculum(curriculum):
            return False

        # If the plan allows all grade levels, return True
        if self.plan.all_grade_levels:
            return True

        # Check if there's a specific access for this class level
        return self.curriculum_accesses.filter(
            curriculum=curriculum,
            class_level=class_level
        ).exists() or self.curriculum_accesses.filter(
            curriculum=curriculum,
            class_level=None
        ).exists()

    def has_access_to_content(self, note):
        """Check if the subscription has access to a specific note."""
        if not self.is_active:
            return False

        # Get the curriculum and class level from the note
        curriculum = note.topic.subject.curriculum
        class_level = note.topic.subject.class_level

        return self.has_access_to_class_level(curriculum, class_level)

    def cancel(self):
        """Cancel the subscription."""
        if self.status == 'active':
            self.status = 'canceled'
            self.canceled_at = timezone.now()
            self.auto_renew = False
            # Clear any scheduled changes
            self.scheduled_plan = None
            self.scheduled_change_type = None
            self.save()

    def schedule_plan_change(self, new_plan, change_type):
        """Schedule a plan change for the end of the current billing period."""
        if self.status != 'active':
            return False

        self.scheduled_plan = new_plan
        self.scheduled_change_type = change_type
        self.save()
        return True

    def cancel_scheduled_change(self):
        """Cancel a scheduled plan change."""
        if self.scheduled_plan:
            self.scheduled_plan = None
            self.scheduled_change_type = None
            self.save()
            return True
        return False

    def upgrade_immediately(self, new_plan):
        """Upgrade to a higher tier plan immediately with proration."""
        if self.status != 'active' or not new_plan:
            return False

        # Calculate remaining days in current subscription
        now = timezone.now()
        remaining_days = (self.end_date - now).days

        # Calculate prorated refund for current plan
        if remaining_days > 0:
            total_period = 30 if self.plan.billing_cycle == 'monthly' else 365
            remaining_ratio = remaining_days / total_period
            prorated_refund = float(self.plan.price) * remaining_ratio
        else:
            prorated_refund = 0

        # Calculate new end date based on new plan's billing cycle
        if new_plan.billing_cycle == 'monthly':
            new_end_date = now + timedelta(days=30)
        else:  # yearly
            new_end_date = now + timedelta(days=365)

        # Apply the change
        self.plan = new_plan
        self.start_date = now
        self.end_date = new_end_date

        # Clear any scheduled changes
        self.scheduled_plan = None
        self.scheduled_change_type = None

        self.save()

        # Return the prorated refund amount for potential credit
        return prorated_refund

    def change_billing_cycle(self, new_plan):
        """Change the billing cycle for the same tier."""
        if self.status != 'active' or not new_plan or new_plan.plan_type != self.plan.plan_type:
            return False

        # Similar to upgrade_immediately but for billing cycle changes
        return self.upgrade_immediately(new_plan)

    def process_scheduled_change(self):
        """Process a scheduled plan change that is due."""
        if not self.scheduled_plan:
            return False

        # Apply the scheduled change
        self.plan = self.scheduled_plan

        # Update dates
        now = timezone.now()
        if self.plan.billing_cycle == 'monthly':
            self.end_date = now + timedelta(days=30)
        else:  # yearly
            self.end_date = now + timedelta(days=365)

        # Clear the scheduled change
        self.scheduled_plan = None
        self.scheduled_change_type = None

        self.save()
        return True

    def toggle_auto_renew(self):
        """Toggle the auto-renew setting."""
        self.auto_renew = not self.auto_renew
        self.save()
        return self.auto_renew


class CurriculumAccess(models.Model):
    """Model representing access to a specific curriculum and class level for a subscription."""

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='curriculum_accesses')
    curriculum = models.ForeignKey('curriculum.Curriculum', on_delete=models.CASCADE)
    class_level = models.ForeignKey('curriculum.ClassLevel', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Curriculum Accesses"
        unique_together = ['subscription', 'curriculum', 'class_level']

    def __str__(self):
        if self.class_level:
            return f"{self.subscription.user.email} - {self.curriculum.name} - {self.class_level.name}"
        return f"{self.subscription.user.email} - {self.curriculum.name} - All Levels"


class Payment(models.Model):
    """Model representing a payment for a subscription."""

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Payment details
    payment_method = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(default=timezone.now)

    # For refunds
    refund_date = models.DateTimeField(null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    refund_reason = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.subscription.user.email} - {self.amount} ({self.get_status_display()})"

    def refund(self, amount=None, reason=''):
        """Process a refund for this payment."""
        if self.status != 'completed':
            return False

        self.status = 'refunded'
        self.refund_date = timezone.now()
        self.refund_amount = amount if amount else self.amount
        self.refund_reason = reason
        self.save()
        return True


class PaymentMethod(models.Model):
    """Model representing a saved payment method."""

    TYPE_CHOICES = (
        ('card', 'Credit/Debit Card'),
        ('bank_account', 'Bank Account'),
        ('mobile_money', 'Mobile Money'),
    )

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='payment_methods')

    # Provider details
    payment_provider = models.CharField(max_length=50)  # e.g., 'stripe', 'paystack'
    provider_payment_method_id = models.CharField(max_length=100)

    # Payment method details
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    brand = models.CharField(max_length=50, blank=True)  # e.g., 'visa', 'mastercard'
    last4 = models.CharField(max_length=4, blank=True)
    exp_month = models.PositiveIntegerField(null=True, blank=True)
    exp_year = models.PositiveIntegerField(null=True, blank=True)

    # For bank accounts
    bank_name = models.CharField(max_length=100, blank=True)
    account_type = models.CharField(max_length=50, blank=True)

    # For mobile money
    phone_number = models.CharField(max_length=20, blank=True)
    mobile_provider = models.CharField(max_length=50, blank=True)

    # Status
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Metadata
    metadata = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_default', '-created_at']
        unique_together = ['user', 'provider_payment_method_id']

    def __str__(self):
        if self.type == 'card':
            return f"{self.brand} •••• {self.last4}"
        elif self.type == 'bank_account':
            return f"{self.bank_name} •••• {self.last4}"
        elif self.type == 'mobile_money':
            return f"{self.mobile_provider} {self.phone_number}"
        return f"Payment Method {self.id}"

    def save(self, *args, **kwargs):
        # If this is set as default, unset any other default for this user
        if self.is_default:
            PaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)

        # If this is the only payment method, make it default
        if not PaymentMethod.objects.filter(user=self.user).exists():
            self.is_default = True

        super().save(*args, **kwargs)
