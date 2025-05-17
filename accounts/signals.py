from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from allauth.account.signals import user_signed_up
import logging

from .models import User
from subscription.models import SubscriptionPlan, Subscription, CurriculumAccess
from curriculum.models import Curriculum, ClassLevel

logger = logging.getLogger(__name__)

@receiver(user_signed_up)
def create_free_subscription(sender, request, user, **kwargs):
    """
    Create a free subscription for new users when they register.
    """
    try:
        # Check if the user already has a subscription
        if Subscription.objects.filter(user=user).exists():
            logger.info(f"User {user.id} already has a subscription. Skipping free subscription creation.")
            return

        # Get the free subscription plan
        free_plan = SubscriptionPlan.objects.filter(
            plan_type='free',
            billing_cycle='monthly',
            is_active=True
        ).first()

        if not free_plan:
            logger.error("No active free subscription plan found. Cannot create free subscription.")
            return

        # Calculate subscription end date (30 days from now)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30)

        # Create the subscription
        subscription = Subscription.objects.create(
            user=user,
            plan=free_plan,
            status='active',
            start_date=start_date,
            end_date=end_date,
            auto_renew=True
        )

        logger.info(f"Created free subscription for user {user.id}")

        # Note: We don't create CurriculumAccess here because we want the user
        # to select their preferred curriculum and class level on the dashboard
        
    except Exception as e:
        logger.exception(f"Error creating free subscription for user {user.id}: {str(e)}")
