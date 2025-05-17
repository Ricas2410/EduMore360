from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
import json
import uuid
import hmac
import hashlib
import requests
import logging
from datetime import timedelta, datetime

from .models import SubscriptionPlan, Subscription, Payment, CurriculumAccess
from accounts.models import User, UserGroup
from curriculum.models import Curriculum, ClassLevel

# Set up logger
logger = logging.getLogger(__name__)


def access_denied(request):
    """View for displaying access denied page."""
    curriculum = None
    class_level = None

    # Get curriculum and class level from query parameters if available
    curriculum_id = request.GET.get('curriculum_id')
    class_level_id = request.GET.get('class_level_id')

    if curriculum_id and class_level_id:
        curriculum = Curriculum.objects.filter(id=curriculum_id).first()
        class_level = ClassLevel.objects.filter(id=class_level_id).first()

    message = request.GET.get('message', "You don't have access to this content with your current subscription plan.")

    context = {
        'message': message,
        'curriculum': curriculum,
        'class_level': class_level,
    }

    return render(request, 'subscription/access_denied.html', context)


def subscription_plans(request):
    """View for displaying subscription plans."""
    # Get all active subscription plans
    monthly_plans = SubscriptionPlan.objects.filter(
        billing_cycle='monthly',
        is_active=True
    ).order_by('price')

    yearly_plans = SubscriptionPlan.objects.filter(
        billing_cycle='yearly',
        is_active=True
    ).order_by('price')

    # Check if user has an active subscription
    has_active_subscription = False
    current_subscription = None
    current_plan_type = None

    if request.user.is_authenticated:
        current_subscription = Subscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()

        has_active_subscription = current_subscription is not None

        if has_active_subscription:
            current_plan_type = current_subscription.plan.plan_type

    context = {
        'monthly_plans': monthly_plans,
        'yearly_plans': yearly_plans,
        'has_active_subscription': has_active_subscription,
        'current_subscription': current_subscription,
        'current_plan_type': current_plan_type,
    }
    return render(request, 'subscription/subscription_plans.html', context)


@login_required
def subscribe(request, plan_type, billing_cycle):
    """View for subscribing to a plan."""
    # Get the subscription plan
    plan = get_object_or_404(SubscriptionPlan, plan_type=plan_type, billing_cycle=billing_cycle, is_active=True)

    # Check if user already has an active subscription
    active_subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if active_subscription:
        # Instead of requiring cancellation, redirect to the change plan page
        messages.info(request, "You already have an active subscription. You can change your plan here.")
        return redirect('subscription:change_plan')

    # For tier_one and tier_two plans, we need to select curriculum and class level
    if plan.plan_type in ['tier_one', 'tier_two'] and request.method == 'GET':
        # Get all available curriculums
        curriculums = Curriculum.objects.filter(is_active=True)

        # For tier_one, we also need to get class levels
        class_levels = None
        selected_curriculum = None

        # If a curriculum is selected, get its class levels
        if 'curriculum' in request.GET:
            selected_curriculum = get_object_or_404(Curriculum, code=request.GET['curriculum'])
            class_levels = ClassLevel.objects.filter(curriculum=selected_curriculum, is_active=True)

        context = {
            'plan': plan,
            'curriculums': curriculums,
            'class_levels': class_levels,
            'selected_curriculum': selected_curriculum,
        }

        if plan.plan_type == 'tier_one':
            return render(request, 'subscription/select_curriculum_class.html', context)
        else:  # tier_two
            return render(request, 'subscription/select_curriculum.html', context)

    # Calculate subscription end date
    start_date = timezone.now()
    if billing_cycle == 'monthly':
        end_date = start_date + timedelta(days=30)
    else:  # yearly
        end_date = start_date + timedelta(days=365)

    # Create a new subscription with pending status
    subscription = Subscription.objects.create(
        user=request.user,
        plan=plan,
        status='pending',  # Set to pending until payment is confirmed
        start_date=start_date,
        end_date=end_date,
        auto_renew=True
    )

    # Handle curriculum and class level selection for different tiers
    if plan.plan_type == 'free':
        # Free tier gets access to a sample curriculum and class level
        # This could be configured in the admin or hardcoded
        sample_curriculum = Curriculum.objects.filter(is_active=True).first()
        sample_class_level = ClassLevel.objects.filter(curriculum=sample_curriculum, is_active=True).first()

        if sample_curriculum and sample_class_level:
            CurriculumAccess.objects.create(
                subscription=subscription,
                curriculum=sample_curriculum,
                class_level=sample_class_level
            )

    elif plan.plan_type == 'tier_one':
        # Tier One: One curriculum, one class level
        curriculum_code = request.POST.get('curriculum')
        class_level_id = request.POST.get('class_level')

        if not curriculum_code or not class_level_id:
            # If not provided, redirect back to selection page
            subscription.delete()  # Clean up the created subscription
            messages.error(request, "Please select a curriculum and class level.")
            return redirect('subscription:subscribe', plan_type=plan_type, billing_cycle=billing_cycle)

        curriculum = get_object_or_404(Curriculum, code=curriculum_code)
        class_level = get_object_or_404(ClassLevel, id=class_level_id, curriculum=curriculum)

        CurriculumAccess.objects.create(
            subscription=subscription,
            curriculum=curriculum,
            class_level=class_level
        )

        # Update user's preferred curriculum and class level
        user = request.user
        user.preferred_curriculum = curriculum
        user.preferred_class_level = class_level
        user.save()

        logger.info(f"Updated user {user.id} preferences to curriculum {curriculum.id} and class level {class_level.id}")

    elif plan.plan_type == 'tier_two':
        # Tier Two: One curriculum, all class levels
        curriculum_code = request.POST.get('curriculum')

        if not curriculum_code:
            # If not provided, redirect back to selection page
            subscription.delete()  # Clean up the created subscription
            messages.error(request, "Please select a curriculum.")
            return redirect('subscription:subscribe', plan_type=plan_type, billing_cycle=billing_cycle)

        curriculum = get_object_or_404(Curriculum, code=curriculum_code)

        # Create access for the curriculum with no specific class level (means all levels)
        CurriculumAccess.objects.create(
            subscription=subscription,
            curriculum=curriculum,
            class_level=None  # None means all class levels
        )

    elif plan.plan_type == 'tier_three':
        # Tier Three: All curriculums, all class levels
        # Set the all_curriculums flag to True
        subscription.plan.all_curriculums = True
        subscription.plan.all_grade_levels = True
        subscription.plan.save()

    # If it's a family or enterprise plan, create a user group
    if plan.plan_type in ['tier_two', 'tier_three']:
        group_name = f"{request.user.get_full_name()}'s {plan.get_plan_type_display()} Group"
        group = UserGroup.objects.create(
            name=group_name,
            group_type='family',  # Use family type for tier_two and tier_three
            admin=request.user
        )
        group.members.add(request.user)
        subscription.is_group_admin = True
        subscription.group = group
        subscription.save()

    # Redirect to payment page
    return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
def payment(request, subscription_id):
    """View for processing payment for a subscription."""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)

    # Check if subscription is already paid
    if Payment.objects.filter(subscription=subscription, status='completed').exists():
        messages.info(request, "This subscription has already been paid for.")
        return redirect('subscription:manage_subscription')

    # Import Paystack API
    from .paystack import paystack

    # Refresh Paystack API keys from SystemConfiguration
    paystack.refresh_keys()

    # Log Paystack API keys for debugging
    if not paystack.public_key or not paystack.secret_key:
        logger.error("Paystack API keys are not properly configured")
        messages.error(request, "Payment gateway is not properly configured. Please contact support.")
        return redirect('subscription:manage_subscription')

    # Log that we're using the keys
    logger.info(f"Using Paystack public key: {paystack.public_key[:10]}...")

    # Get payment link
    payment_link = paystack.get_payment_link(request, subscription)

    if not payment_link:
        logger.error(f"Failed to generate Paystack payment link for subscription {subscription.id}")
        messages.error(request, "Failed to generate payment link. Please try again or contact support.")
        return redirect('subscription:manage_subscription')

    # Calculate amount in GHS
    exchange_rate = getattr(settings, 'USD_TO_GHS_RATE', 11.5)
    amount_ghs = float(subscription.plan.price) * exchange_rate
    amount_pesewas = int(amount_ghs * 100)  # Convert to pesewas

    context = {
        'subscription': subscription,
        'paystack_public_key': paystack.public_key,
        'callback_url': request.build_absolute_uri(reverse('subscription:payment_success', args=[subscription.id])),
        'amount': amount_pesewas,  # Amount in pesewas
        'payment_link': payment_link,
    }
    return render(request, 'subscription/payment.html', context)


@login_required
def payment_success(request, subscription_id):
    """View for handling successful payment."""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)

    # Get payment reference from query parameters
    reference = request.GET.get('reference')

    if not reference:
        messages.error(request, "No payment reference provided.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    # Check if payment already exists
    existing_payment = Payment.objects.filter(
        transaction_id=reference,
        status='completed'
    ).first()

    if existing_payment:
        messages.success(request, "Your payment has already been processed. Your subscription is active.")
        return redirect('subscription:manage_subscription')

    # Import Paystack API
    from .paystack import paystack

    # Refresh Paystack API keys from SystemConfiguration
    paystack.refresh_keys()

    # Verify payment with Paystack
    transaction_data = paystack.verify_transaction(reference)

    if not transaction_data:
        messages.error(request, "Payment verification failed. Please try again or contact support.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    # Check if payment was successful
    if transaction_data['status'] == 'success':
        # Get the amount paid in GHS
        amount_paid_ghs = transaction_data['amount'] / 100  # Convert from pesewas to GHS

        # Check if there's original currency info in metadata
        original_currency = None
        original_amount = None
        if 'metadata' in transaction_data and transaction_data['metadata']:
            metadata = transaction_data['metadata']
            original_currency = metadata.get('original_currency')
            original_amount = metadata.get('original_amount')

        # If we have original USD amount, use it for comparison
        if original_currency == 'USD' and original_amount is not None:
            amount_paid = float(original_amount)
            expected_amount = float(subscription.plan.price)
            currency_display = 'USD'
        else:
            # Otherwise, we need to convert GHS back to USD for comparison
            # Get the exchange rate from settings or use a default
            exchange_rate = getattr(settings, 'USD_TO_GHS_RATE', 11.5)
            amount_paid = amount_paid_ghs / exchange_rate
            expected_amount = float(subscription.plan.price)
            currency_display = 'USD'

        # Allow for small differences due to currency conversion (5% tolerance)
        tolerance = expected_amount * 0.05
        if abs(amount_paid - expected_amount) > tolerance:
            logger.warning(f"Payment amount mismatch: expected {expected_amount} {currency_display}, got {amount_paid} {currency_display}")
            messages.warning(request, "Payment amount doesn't match subscription price. Please contact support.")

        # Verify that the email matches the user's email
        customer_email = transaction_data['customer']['email']
        if customer_email.lower() != request.user.email.lower():
            logger.warning(f"Email mismatch: expected {request.user.email}, got {customer_email}")
            messages.warning(request, "Payment email doesn't match your account. Please contact support.")

        # Create payment record
        payment = Payment.objects.create(
            subscription=subscription,
            amount=amount_paid,
            status='completed',
            payment_method='Paystack',
            transaction_id=reference
        )

        # Update subscription status
        subscription.status = 'active'

        # If it's a family plan, ensure the user is set as a group admin
        if subscription.plan.plan_type == 'family' and subscription.group:
            subscription.is_group_admin = True

        subscription.save()

        # Update user's premium status
        user = subscription.user
        user.is_premium = True
        user.subscription_end_date = subscription.end_date

        # If it's a tier_one subscription, ensure user preferences are set
        if subscription.plan.plan_type == 'tier_one':
            # Get the curriculum access for this subscription
            curriculum_access = subscription.curriculum_accesses.first()
            if curriculum_access:
                # Update user preferences if not already set
                if not user.preferred_curriculum or not user.preferred_class_level:
                    user.preferred_curriculum = curriculum_access.curriculum
                    user.preferred_class_level = curriculum_access.class_level
                    logger.info(f"Updated user {user.id} preferences during payment success")

        user.save()

        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Subscription Activated",
            message=f"Your {subscription.plan.name} subscription has been activated.",
            notification_type='success',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )

        # Log successful payment
        logger.info(f"Payment {reference} for user {user.email} completed successfully")

        messages.success(request, "Payment successful! Your subscription is now active.")
        return redirect('subscription:manage_subscription')
    else:
        # Log the error
        error_message = transaction_data.get('gateway_response', 'Unknown error')
        logger.error(f"Payment verification failed: {error_message}")

        messages.error(request, "Payment verification failed. Please try again or contact support.")
        return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
def payment_cancel(request, subscription_id):
    """View for handling cancelled payment."""
    # Get the subscription regardless of status
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)

    # Log the subscription details for debugging
    logger.info(f"Cancelling subscription {subscription_id} with status {subscription.status}")

    # Store the original status for messaging
    original_status = subscription.status

    # If the subscription is pending, delete it instead of just marking it as canceled
    if original_status == 'pending':
        # Store subscription details for logging
        subscription_details = {
            'id': subscription.id,
            'plan': subscription.plan.name,
            'status': subscription.status,
            'user': subscription.user.email
        }

        # Delete the subscription
        subscription.delete()

        # Log the deletion
        logger.info(f"Deleted pending subscription {subscription_details}")

        # Create notification about the cancellation
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Subscription Cancelled",
            message=f"Your pending subscription has been cancelled.",
            notification_type='info',
            category='subscription',
            url=reverse('subscription:subscription_plans')
        )
    else:
        # Update subscription status
        subscription.status = 'canceled'
        subscription.save()

        # Log the update
        logger.info(f"Updated subscription {subscription_id} status to 'canceled'")

    # If the subscription wasn't deleted and has a group, remove it
    if original_status != 'pending' and subscription.group:
        group = subscription.group
        subscription.group = None
        subscription.is_group_admin = False
        subscription.save()

        # Log group removal
        logger.info(f"Removed group association from subscription {subscription_id}")

        # Delete the group if it was created for this subscription
        if group.admin == request.user:
            group.delete()
            logger.info(f"Deleted group for subscription {subscription_id}")

    # Update user's premium status if needed
    user = request.user  # Use request.user instead of subscription.user in case subscription was deleted
    if user.is_premium:
        # Check if user has any other active subscriptions
        other_active_subscription = Subscription.objects.filter(
            user=user,
            status='active',
            end_date__gt=timezone.now()
        )

        # If we still have the subscription object, exclude it from the check
        if original_status != 'pending':
            other_active_subscription = other_active_subscription.exclude(id=subscription.id)

        # Check if any active subscriptions exist
        if not other_active_subscription.exists():
            user.is_premium = False
            user.subscription_end_date = None
            user.save()
            logger.info(f"Updated user {user.id} premium status to False")

    # Delete any pending payments for this subscription
    if original_status == 'pending':
        # For pending subscriptions that were deleted, find payments by subscription ID
        pending_payments = Payment.objects.filter(
            subscription_id=subscription_id,
            status='pending'
        )
    else:
        # For other subscriptions, use the subscription object
        pending_payments = Payment.objects.filter(
            subscription=subscription,
            status='pending'
        )

    if pending_payments.exists():
        count = pending_payments.count()
        pending_payments.delete()
        logger.info(f"Deleted {count} pending payments for subscription {subscription_id}")

    if original_status == 'pending':
        messages.info(request, "Payment cancelled. Your subscription has been removed.")
    else:
        messages.info(request, "Payment cancelled. Your subscription has not been activated.")

    # Redirect to subscription plans page
    return redirect('subscription:subscription_plans')


@csrf_exempt
@require_http_methods(["POST"])
def payment_webhook(request):
    """Webhook for handling Paystack payment notifications."""
    # Get Paystack signature from headers
    paystack_signature = request.headers.get('X-Paystack-Signature')

    if not paystack_signature:
        logger.error("Webhook received without signature")
        return HttpResponse("No signature provided", status=400)

    # Get request body
    payload = request.body

    # Import Paystack API
    from .paystack import paystack

    # Refresh Paystack API keys from SystemConfiguration
    paystack.refresh_keys()

    # Verify signature
    if not paystack.verify_webhook_signature(payload, paystack_signature):
        logger.error("Invalid webhook signature")
        return HttpResponse("Invalid signature", status=400)

    # Parse payload
    try:
        event_data = json.loads(payload)
        event = event_data.get('event')

        # Log the event for debugging
        logger.info(f"Received Paystack webhook: {event}")

        if event == 'charge.success':
            # Get reference
            reference = event_data['data']['reference']

            # Get customer data
            customer_email = event_data['data']['customer']['email']
            amount = event_data['data']['amount'] / 100  # Convert from kobo/cents to main currency

            # Find payment by reference
            payment = Payment.objects.filter(transaction_id=reference).first()

            if payment:
                # Update payment status if not already completed
                if payment.status != 'completed':
                    payment.status = 'completed'
                    payment.save()

                    # Update subscription status
                    subscription = payment.subscription
                    if subscription.status != 'active':
                        subscription.status = 'active'
                        subscription.save()

                    # Update user's premium status
                    user = subscription.user
                    user.is_premium = True
                    user.subscription_end_date = subscription.end_date

                    # If it's a tier_one subscription, ensure user preferences are set
                    if subscription.plan.plan_type == 'tier_one':
                        # Get the curriculum access for this subscription
                        curriculum_access = subscription.curriculum_accesses.first()
                        if curriculum_access:
                            # Update user preferences if not already set
                            if not user.preferred_curriculum or not user.preferred_class_level:
                                user.preferred_curriculum = curriculum_access.curriculum
                                user.preferred_class_level = curriculum_access.class_level
                                logger.info(f"Updated user {user.id} preferences during webhook processing")

                    user.save()

                    # Create notification
                    from core.models import Notification
                    Notification.objects.create(
                        user=user,
                        title="Payment Successful",
                        message=f"Your payment of {amount} for the {subscription.plan.name} subscription was successful.",
                        notification_type='success',
                        category='subscription',
                        url=reverse('subscription:manage_subscription')
                    )

                    logger.info(f"Payment {reference} for {customer_email} marked as completed")
                else:
                    logger.info(f"Payment {reference} already completed")
            else:
                # Payment not found, try to find subscription by reference
                # This can happen if the webhook arrives before the payment_success view is called
                from accounts.models import User
                user = User.objects.filter(email=customer_email).first()

                if user:
                    # Find active or pending subscription
                    subscription = Subscription.objects.filter(
                        user=user,
                        status__in=['active', 'pending'],
                        end_date__gt=timezone.now()
                    ).order_by('-created_at').first()

                    if subscription:
                        # Create payment record
                        new_payment = Payment.objects.create(
                            subscription=subscription,
                            amount=amount,
                            status='completed',
                            payment_method='Paystack',
                            transaction_id=reference
                        )

                        # Update subscription status
                        if subscription.status != 'active':
                            subscription.status = 'active'
                            subscription.save()

                        # Update user's premium status
                        user.is_premium = True
                        user.subscription_end_date = subscription.end_date

                        # If it's a tier_one subscription, ensure user preferences are set
                        if subscription.plan.plan_type == 'tier_one':
                            # Get the curriculum access for this subscription
                            curriculum_access = subscription.curriculum_accesses.first()
                            if curriculum_access:
                                # Update user preferences if not already set
                                if not user.preferred_curriculum or not user.preferred_class_level:
                                    user.preferred_curriculum = curriculum_access.curriculum
                                    user.preferred_class_level = curriculum_access.class_level
                                    logger.info(f"Updated user {user.id} preferences during webhook processing (second case)")

                        user.save()

                        # Create notification
                        from core.models import Notification
                        Notification.objects.create(
                            user=user,
                            title="Payment Successful",
                            message=f"Your payment of {amount} for the {subscription.plan.name} subscription was successful.",
                            notification_type='success',
                            category='subscription',
                            url=reverse('subscription:manage_subscription')
                        )

                        logger.info(f"Created payment {reference} for {customer_email}")
                    else:
                        # No active subscription found, create a new one with the default plan
                        default_plan = SubscriptionPlan.objects.filter(is_default=True).first()

                        if default_plan:
                            # Calculate end date
                            start_date = timezone.now().date()
                            if default_plan.billing_cycle == 'monthly':
                                end_date = start_date + timedelta(days=30)
                            elif default_plan.billing_cycle == 'quarterly':
                                end_date = start_date + timedelta(days=90)
                            elif default_plan.billing_cycle == 'annual':
                                end_date = start_date + timedelta(days=365)
                            else:
                                end_date = start_date + timedelta(days=30)

                            # Create subscription
                            new_subscription = Subscription.objects.create(
                                user=user,
                                plan=default_plan,
                                status='active',
                                start_date=start_date,
                                end_date=end_date,
                                auto_renew=True
                            )

                            # Create payment record
                            new_payment = Payment.objects.create(
                                subscription=new_subscription,
                                amount=amount,
                                status='completed',
                                payment_method='Paystack',
                                transaction_id=reference
                            )

                            # Update user's premium status
                            user.is_premium = True
                            user.subscription_end_date = end_date
                            user.save()

                            # Create notification
                            from core.models import Notification
                            Notification.objects.create(
                                user=user,
                                title="Subscription Activated",
                                message=f"Your {default_plan.name} subscription has been activated.",
                                notification_type='success',
                                category='subscription',
                                url=reverse('subscription:manage_subscription')
                            )

                            logger.info(f"Created new subscription and payment {reference} for {customer_email}")
                        else:
                            logger.error(f"No default plan found for automatic subscription creation")
                else:
                    logger.warning(f"User with email {customer_email} not found")

        elif event == 'subscription.create':
            # Handle subscription creation
            reference = event_data['data']['subscription_code']
            customer_email = event_data['data']['customer']['email']
            plan_code = event_data['data']['plan']['plan_code']

            # Log subscription creation
            logger.info(f"Subscription {reference} created for {customer_email} with plan {plan_code}")

        elif event == 'subscription.disable':
            # Handle subscription cancellation
            reference = event_data['data']['subscription_code']
            customer_email = event_data['data']['customer']['email']

            # Find user by email
            from accounts.models import User
            user = User.objects.filter(email=customer_email).first()

            if user:
                # Find active subscription
                subscription = Subscription.objects.filter(
                    user=user,
                    status='active'
                ).first()

                if subscription:
                    # Cancel subscription
                    subscription.status = 'canceled'
                    subscription.auto_renew = False
                    subscription.save()

                    # Create notification
                    from core.models import Notification
                    Notification.objects.create(
                        user=user,
                        title="Subscription Cancelled",
                        message=f"Your {subscription.plan.name} subscription has been cancelled. You will still have access until {subscription.end_date}.",
                        notification_type='info',
                        category='subscription',
                        url=reverse('subscription:manage_subscription')
                    )

                    logger.info(f"Subscription {reference} for {customer_email} cancelled")
                else:
                    logger.warning(f"No active subscription found for {customer_email}")
            else:
                logger.warning(f"User with email {customer_email} not found")

        elif event == 'transfer.success':
            # Handle successful transfer (e.g., refund)
            reference = event_data['data']['reference']
            amount = event_data['data']['amount'] / 100

            # Log transfer
            logger.info(f"Transfer {reference} for {amount} successful")

        elif event == 'transfer.failed':
            # Handle failed transfer
            reference = event_data['data']['reference']
            reason = event_data['data'].get('reason', 'Unknown reason')

            # Log failed transfer
            logger.warning(f"Transfer {reference} failed: {reason}")

        # Return success for all events
        return HttpResponse("Webhook received", status=200)

    except json.JSONDecodeError:
        logger.error(f"Invalid JSON payload in webhook: {payload}")
        return HttpResponse("Invalid JSON payload", status=400)
    except KeyError as e:
        logger.error(f"Missing required field in webhook: {str(e)}")
        return HttpResponse(f"Missing required field: {str(e)}", status=400)
    except Exception as e:
        # Log the error
        logger.exception(f"Error processing webhook: {str(e)}")
        return HttpResponse(str(e), status=500)


@login_required
def manage_subscription(request):
    """View for managing subscription."""
    # Get user's active subscription
    subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    # If no active subscription, check for pending subscriptions
    pending_subscription = None
    if not subscription:
        pending_subscription = Subscription.objects.filter(
            user=request.user,
            status='pending'
        ).order_by('-created_at').first()

    # Get payment history
    payments = Payment.objects.filter(
        subscription__user=request.user
    ).order_by('-payment_date')[:5]

    # Check if user is a member of any group
    group_memberships = UserGroup.objects.filter(members=request.user)

    # Get family members if user is a group admin
    family_members = None
    if subscription and subscription.plan.plan_type == 'family':
        # Ensure the user is set as a group admin
        if subscription.group and not subscription.is_group_admin:
            subscription.is_group_admin = True
            subscription.save()

        # Get family members
        if subscription.group:
            family_members = subscription.group.members.exclude(id=request.user.id)

    context = {
        'subscription': subscription,
        'pending_subscription': pending_subscription,
        'payments': payments,
        'group_memberships': group_memberships,
        'family_members': family_members,
    }
    return render(request, 'subscription/manage_subscription.html', context)


@login_required
def cancel_subscription(request, subscription_id=None):
    """View for cancelling subscription."""
    if request.method != 'POST':
        return redirect('subscription:manage_subscription')

    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Get user's active subscription
    if subscription_id:
        subscription = get_object_or_404(
            Subscription,
            id=subscription_id,
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        )
    else:
        subscription = Subscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()

    if not subscription:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': "You don't have an active subscription to cancel."
            }, status=400)
        messages.error(request, "You don't have an active subscription to cancel.")
        return redirect('subscription:manage_subscription')

    try:
        # Cancel subscription
        subscription.status = 'canceled'
        subscription.auto_renew = False
        subscription.save()

        # If user is a group admin, cancel the group
        if subscription.is_group_admin and subscription.group:
            # Update all members' subscriptions
            member_subscriptions = Subscription.objects.filter(group=subscription.group)
            for member_sub in member_subscriptions:
                if member_sub.id != subscription.id:  # Skip the admin's subscription as it's already canceled
                    member_sub.status = 'canceled'
                    member_sub.auto_renew = False
                    member_sub.save()

        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': "Your subscription has been cancelled. You will still have access until the end of your billing period."
            })

        messages.success(request, "Your subscription has been cancelled. You will still have access until the end of your billing period.")
        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error canceling subscription: {str(e)}")
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': "An error occurred while canceling your subscription. Please try again."
            }, status=500)
        messages.error(request, "An error occurred while canceling your subscription. Please try again.")
        return redirect('subscription:manage_subscription')


@login_required
def change_plan(request):
    """View for changing subscription plan (upgrade, downgrade, or change billing cycle)."""
    # Get user's active subscription
    subscription = Subscription.objects.filter(
        user=request.user,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if not subscription:
        messages.error(request, "You don't have an active subscription to change.")
        return redirect('subscription:subscription_plans')

    # Handle form submission
    if request.method == 'POST':
        plan_id = request.POST.get('plan_id')
        action = request.POST.get('action')

        if not plan_id or not action:
            messages.error(request, "Invalid request. Please try again.")
            return redirect('subscription:change_plan')

        try:
            new_plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)

            if action == 'upgrade':
                # Immediate upgrade
                prorated_refund = subscription.upgrade_immediately(new_plan)
                messages.success(request, f"Your subscription has been upgraded to {new_plan.name}.")

                # If there was a prorated refund, show it
                if prorated_refund > 0:
                    messages.info(request, f"A credit of ${prorated_refund:.2f} has been applied to your account.")

                return redirect('subscription:manage_subscription')

            elif action == 'downgrade':
                # Schedule downgrade for end of billing period
                subscription.schedule_plan_change(new_plan, 'downgrade')
                messages.success(request, f"Your subscription will be downgraded to {new_plan.name} at the end of your current billing period.")

                # Get the scheduled plan for the template
                scheduled_plan = new_plan
                return render(request, 'subscription/scheduled_change.html', {
                    'current_subscription': subscription,
                    'scheduled_plan': scheduled_plan
                })

            elif action == 'change_billing':
                # Change billing cycle
                subscription.change_billing_cycle(new_plan)
                messages.success(request, f"Your subscription billing cycle has been changed to {new_plan.get_billing_cycle_display()}.")
                return redirect('subscription:manage_subscription')

            else:
                messages.error(request, "Invalid action. Please try again.")
                return redirect('subscription:change_plan')

        except SubscriptionPlan.DoesNotExist:
            messages.error(request, "The selected plan does not exist or is not active.")
            return redirect('subscription:change_plan')

    # Get all active plans except the current one
    current_plan = subscription.plan
    all_plans = SubscriptionPlan.objects.filter(is_active=True).exclude(
        id=current_plan.id
    ).order_by('plan_type', 'billing_cycle')

    # Check if there's a scheduled change
    if subscription.scheduled_plan:
        return render(request, 'subscription/scheduled_change.html', {
            'current_subscription': subscription,
            'scheduled_plan': subscription.scheduled_plan
        })

    context = {
        'current_subscription': subscription,
        'upgrade_plans': all_plans
    }

    return render(request, 'subscription/change_plan.html', context)


@login_required
def cancel_scheduled_change(request, subscription_id):
    """View for canceling a scheduled plan change."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user,
        status='active'
    )

    if request.method == 'POST':
        if subscription.scheduled_plan:
            plan_name = subscription.scheduled_plan.name
            subscription.cancel_scheduled_change()
            messages.success(request, f"Your scheduled change to {plan_name} has been canceled.")
        else:
            messages.warning(request, "You don't have any scheduled plan changes.")

    return redirect('subscription:manage_subscription')


@login_required
def toggle_auto_renew(request, subscription_id):
    """View for toggling auto-renew for a subscription."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user
    )

    if request.method == 'POST':
        auto_renew = subscription.toggle_auto_renew()

        if auto_renew:
            messages.success(request, "Auto-renewal has been turned on. Your subscription will automatically renew at the end of your billing period.")
        else:
            messages.success(request, "Auto-renewal has been turned off. Your subscription will expire at the end of your billing period.")

    return redirect('subscription:manage_subscription')


@login_required
def group_members(request):
    """View for managing group members."""
    # Check if user is a group admin
    subscription = Subscription.objects.filter(
        user=request.user,
        is_group_admin=True,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if not subscription or not subscription.group:
        messages.error(request, "You are not an admin of any group subscription.")
        return redirect('subscription:manage_subscription')

    group = subscription.group
    members = group.members.all()

    # Calculate available slots
    max_members = subscription.plan.max_users
    available_slots = max_members - members.count()

    context = {
        'subscription': subscription,
        'group': group,
        'members': members,
        'available_slots': available_slots,
        'max_members': max_members,
    }
    return render(request, 'subscription/group_members.html', context)


@login_required
def add_group_member(request):
    """View for adding a member to a group."""
    if request.method != 'POST':
        return redirect('subscription:group_members')

    # Check if this is an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    # Check if user is a group admin
    subscription = Subscription.objects.filter(
        user=request.user,
        is_group_admin=True,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if not subscription or not subscription.group:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': "You are not an admin of any group subscription."
            })
        messages.error(request, "You are not an admin of any group subscription.")
        return redirect('subscription:manage_subscription')

    group = subscription.group

    # Check if group has reached maximum members
    if group.members.count() >= subscription.plan.max_users:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': f"Your {subscription.plan.get_plan_type_display()} plan has reached the maximum number of members ({subscription.plan.max_users})."
            })
        messages.error(request, f"Your {subscription.plan.get_plan_type_display()} plan has reached the maximum number of members ({subscription.plan.max_users}).")
        return redirect('subscription:group_members')

    # Get email from form
    email = request.POST.get('email')

    if not email:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': "Please provide an email address."
            })
        messages.error(request, "Please provide an email address.")
        return redirect('subscription:group_members')

    # Check if user exists
    try:
        member = User.objects.get(email=email)
    except User.DoesNotExist:
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': f"No user found with email {email}. They need to register first."
            })
        messages.error(request, f"No user found with email {email}. They need to register first.")
        return redirect('subscription:group_members')

    # Check if user is already a member
    if group.members.filter(id=member.id).exists():
        if is_ajax:
            return JsonResponse({
                'success': False,
                'message': f"{email} is already a member of your group."
            })
        messages.warning(request, f"{email} is already a member of your group.")
        return redirect('subscription:group_members')

    # Add user to group
    group.members.add(member)

    # Create or update member's subscription
    member_subscription, created = Subscription.objects.get_or_create(
        user=member,
        defaults={
            'plan': subscription.plan,
            'status': 'active',
            'start_date': subscription.start_date,
            'end_date': subscription.end_date,
            'auto_renew': False,
            'is_group_admin': False,
            'group': group,
        }
    )

    if not created:
        # Update existing subscription
        member_subscription.plan = subscription.plan
        member_subscription.status = 'active'
        member_subscription.start_date = subscription.start_date
        member_subscription.end_date = subscription.end_date
        member_subscription.auto_renew = False
        member_subscription.is_group_admin = False
        member_subscription.group = group
        member_subscription.save()

    # Update member's premium status
    member.is_premium = True
    member.subscription_end_date = subscription.end_date
    member.save()

    if is_ajax:
        return JsonResponse({
            'success': True,
            'message': f"{email} has been added to your group successfully."
        })

    messages.success(request, f"{email} has been added to your group.")
    return redirect('subscription:group_members')


@login_required
def remove_group_member(request, user_id):
    """View for removing a member from a group."""
    if request.method != 'POST':
        return redirect('subscription:group_members')

    # Check if user is a group admin
    subscription = Subscription.objects.filter(
        user=request.user,
        is_group_admin=True,
        status='active',
        end_date__gt=timezone.now()
    ).first()

    if not subscription or not subscription.group:
        messages.error(request, "You are not an admin of any group subscription.")
        return redirect('subscription:manage_subscription')

    group = subscription.group

    # Get member
    member = get_object_or_404(User, id=user_id)

    # Check if member is in the group
    if not group.members.filter(id=member.id).exists():
        messages.error(request, "This user is not a member of your group.")
        return redirect('subscription:group_members')

    # Check if member is the admin
    if member.id == request.user.id:
        messages.error(request, "You cannot remove yourself from the group. Please cancel the subscription instead.")
        return redirect('subscription:group_members')

    # Remove member from group
    group.members.remove(member)

    # Update member's subscription
    member_subscription = Subscription.objects.filter(
        user=member,
        group=group
    ).first()

    if member_subscription:
        member_subscription.status = 'canceled'
        member_subscription.save()

    # Update member's premium status
    member.is_premium = False
    member.subscription_end_date = None
    member.save()

    messages.success(request, f"{member.email} has been removed from your group.")
    return redirect('subscription:group_members')


@login_required
def payment_history(request):
    """View for showing payment history."""
    # Get all payments for the user
    payments = Payment.objects.filter(
        subscription__user=request.user
    ).order_by('-payment_date')

    context = {
        'payments': payments,
    }
    return render(request, 'subscription/payment_history.html', context)


@login_required
def invoice(request, payment_id):
    """View for showing invoice for a payment."""
    payment = get_object_or_404(Payment, id=payment_id, subscription__user=request.user)

    context = {
        'payment': payment,
        'subscription': payment.subscription,
    }
    return render(request, 'subscription/invoice.html', context)


@login_required
@require_POST
def process_payment(request, subscription_id):
    """Process a credit card payment for a subscription."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user,
        status__in=['pending', 'active']
    )

    # Get payment method ID
    payment_method_id = request.POST.get('payment_method_id')

    if not payment_method_id:
        messages.error(request, "No payment method provided.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    try:
        # In a real implementation, you would use the Stripe API to process the payment
        # For this example, we'll create a payment record directly

        # Create payment record
        payment = Payment.objects.create(
            subscription=subscription,
            amount=float(subscription.plan.price),
            status='completed',
            payment_method='Credit Card',
            transaction_id=f"cc_{uuid.uuid4().hex[:8]}"
        )

        # Update subscription status
        subscription.status = 'active'
        subscription.save()

        # Update user's premium status
        user = subscription.user
        user.is_premium = True
        user.subscription_end_date = subscription.end_date
        user.save()

        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Subscription Activated",
            message=f"Your {subscription.plan.name} subscription has been activated.",
            notification_type='success',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )

        messages.success(request, "Payment successful! Your subscription is now active.")
        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error processing credit card payment: {str(e)}")
        messages.error(request, f"An error occurred while processing your payment. Please try again.")
        return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
@require_POST
def process_mobile_money(request, subscription_id):
    """Process a mobile money payment for a subscription."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user,
        status__in=['pending', 'active']
    )

    # Get payment details
    phone_number = request.POST.get('phone_number')
    provider = request.POST.get('provider')

    if not phone_number or not provider:
        messages.error(request, "Please provide all required information.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    try:
        # In a real implementation, you would use a mobile money API to process the payment
        # For this example, we'll create a pending payment record

        # Create payment record
        payment = Payment.objects.create(
            subscription=subscription,
            amount=float(subscription.plan.price),
            status='pending',
            payment_method=f"{provider.upper()} Mobile Money",
            transaction_id=f"mm_{uuid.uuid4().hex[:8]}",
            metadata={
                'phone_number': phone_number,
                'provider': provider
            }
        )

        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Payment Processing",
            message=f"Your mobile money payment for the {subscription.plan.name} subscription is being processed. You will be notified once it's complete.",
            notification_type='info',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )

        messages.success(request, "Your payment is being processed. You will be notified once it's complete.")
        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error processing mobile money payment: {str(e)}")
        messages.error(request, f"An error occurred while processing your payment. Please try again.")
        return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
@require_POST
def process_bank_transfer(request, subscription_id):
    """Process a bank transfer payment for a subscription."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user,
        status__in=['pending', 'active']
    )

    # Get payment details
    transfer_reference = request.POST.get('transfer_reference')
    transfer_date = request.POST.get('transfer_date')

    if not transfer_reference or not transfer_date:
        messages.error(request, "Please provide all required information.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    try:
        # Create payment record
        payment = Payment.objects.create(
            subscription=subscription,
            amount=float(subscription.plan.price),
            status='pending',
            payment_method='Bank Transfer',
            transaction_id=f"bt_{uuid.uuid4().hex[:8]}",
            metadata={
                'transfer_reference': transfer_reference,
                'transfer_date': transfer_date
            }
        )

        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Payment Processing",
            message=f"Your bank transfer for the {subscription.plan.name} subscription is being verified. You will be notified once it's complete.",
            notification_type='info',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )

        messages.success(request, "Your bank transfer is being verified. You will be notified once it's complete.")
        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error processing bank transfer: {str(e)}")
        messages.error(request, f"An error occurred while processing your payment. Please try again.")
        return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
@require_POST
def process_paystack_payment(request, subscription_id):
    """Process a Paystack payment for a subscription."""
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user,
        status__in=['pending', 'active']
    )

    # Get payment reference
    reference = request.POST.get('reference')

    if not reference:
        messages.error(request, "No payment reference provided.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    # Import Paystack API
    from .paystack import paystack

    # Refresh Paystack API keys from SystemConfiguration
    paystack.refresh_keys()

    # Verify payment with Paystack
    transaction_data = paystack.verify_transaction(reference)

    if not transaction_data:
        messages.error(request, "Payment verification failed. Please try again or contact support.")
        return redirect('subscription:payment', subscription_id=subscription.id)

    # Check if payment was successful
    if transaction_data['status'] == 'success':
        # Verify that the amount paid matches the subscription price
        amount_paid = transaction_data['amount'] / 100  # Convert from kobo/cents
        expected_amount = float(subscription.plan.price)

        # Allow for small differences due to currency conversion
        if abs(amount_paid - expected_amount) > 1:
            logger.warning(f"Payment amount mismatch: expected {expected_amount}, got {amount_paid}")
            messages.warning(request, "Payment amount doesn't match subscription price. Please contact support.")

        # Verify that the email matches the user's email
        customer_email = transaction_data['customer']['email']
        if customer_email.lower() != request.user.email.lower():
            logger.warning(f"Email mismatch: expected {request.user.email}, got {customer_email}")
            messages.warning(request, "Payment email doesn't match your account. Please contact support.")

        # Create payment record
        payment = Payment.objects.create(
            subscription=subscription,
            amount=amount_paid,
            status='completed',
            payment_method='Paystack',
            transaction_id=reference
        )

        # Update subscription status
        subscription.status = 'active'

        # If it's a family plan, ensure the user is set as a group admin
        if subscription.plan.plan_type == 'family' and subscription.group:
            subscription.is_group_admin = True

        subscription.save()

        # Update user's premium status
        user = subscription.user
        user.is_premium = True
        user.subscription_end_date = subscription.end_date
        user.save()

        # Create notification
        from core.models import Notification
        Notification.objects.create(
            user=request.user,
            title="Subscription Activated",
            message=f"Your {subscription.plan.name} subscription has been activated.",
            notification_type='success',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )

        messages.success(request, "Payment successful! Your subscription is now active.")
        return redirect('subscription:manage_subscription')
    else:
        # Log the error
        error_message = transaction_data.get('gateway_response', 'Unknown error')
        logger.error(f"Payment verification failed: {error_message}")

        messages.error(request, "Payment verification failed. Please try again or contact support.")
        return redirect('subscription:payment', subscription_id=subscription.id)


@login_required
@require_POST
def cancel_subscription(request, subscription_id):
    """View for canceling a subscription."""
    # Get user's active subscription
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user
    )

    if subscription.status != 'active':
        messages.error(request, "This subscription is not active.")
        return redirect('subscription:manage_subscription')

    # For future implementation: Cancel subscription with payment provider if needed
    # Currently, we don't have provider_subscription_id in the Subscription model
    # This would be implemented when integrating with a payment provider's subscription API

    # Cancel subscription in our system
    subscription.status = 'canceled'
    subscription.auto_renew = False
    subscription.save()

    # Create notification
    from core.models import Notification
    Notification.objects.create(
        user=request.user,
        title="Subscription Canceled",
        message=f"Your {subscription.plan.name} subscription has been canceled. You will still have access until {subscription.end_date.strftime('%B %d, %Y')}.",
        notification_type='info',
        category='subscription',
        url=reverse('subscription:manage_subscription')
    )

    messages.success(request, "Your subscription has been canceled. You will still have access until the end of your current billing period.")

    # Return HTML for HTMX
    if request.headers.get('HX-Request'):
        return render(request, 'subscription/partials/subscription_actions.html', {'subscription': subscription})

    return redirect('subscription:manage_subscription')


@login_required
@require_POST
def toggle_auto_renew(request, subscription_id):
    """View for toggling auto-renew for a subscription."""
    # Get user's subscription
    subscription = get_object_or_404(
        Subscription,
        id=subscription_id,
        user=request.user
    )

    # Toggle auto-renew
    subscription.auto_renew = not subscription.auto_renew
    subscription.save()

    # Create notification
    from core.models import Notification
    if subscription.auto_renew:
        Notification.objects.create(
            user=request.user,
            title="Auto-renew Enabled",
            message=f"Auto-renew has been enabled for your {subscription.plan.name} subscription. It will automatically renew on {subscription.end_date.strftime('%B %d, %Y')}.",
            notification_type='info',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )
        messages.success(request, "Auto-renew has been enabled for your subscription.")
    else:
        Notification.objects.create(
            user=request.user,
            title="Auto-renew Disabled",
            message=f"Auto-renew has been disabled for your {subscription.plan.name} subscription. It will expire on {subscription.end_date.strftime('%B %d, %Y')}.",
            notification_type='info',
            category='subscription',
            url=reverse('subscription:manage_subscription')
        )
        messages.success(request, "Auto-renew has been disabled for your subscription.")

    # Return HTML for HTMX
    if request.headers.get('HX-Request'):
        return render(request, 'subscription/partials/subscription_actions.html', {'subscription': subscription})

    return redirect('subscription:manage_subscription')


@login_required
@require_POST
def add_payment_method(request):
    """View for adding a payment method."""
    # Get payment method ID
    payment_method_id = request.POST.get('payment_method_id')
    set_default = request.POST.get('set_default') == 'true'

    if not payment_method_id:
        messages.error(request, "No payment method provided.")
        return redirect('subscription:manage_subscription')

    try:
        # In a real implementation, you would use the Stripe API to attach the payment method to the customer
        # For this example, we'll create a payment method record directly

        # Check if payment method already exists
        from .models import PaymentMethod
        existing_method = PaymentMethod.objects.filter(
            user=request.user,
            provider_payment_method_id=payment_method_id
        ).first()

        if existing_method:
            messages.info(request, "This payment method is already saved to your account.")

            # Set as default if requested
            if set_default and not existing_method.is_default:
                # Unset any existing default
                PaymentMethod.objects.filter(user=request.user, is_default=True).update(is_default=False)

                # Set this one as default
                existing_method.is_default = True
                existing_method.save()

                messages.success(request, "Payment method set as default.")
        else:
            # Create new payment method
            # In a real implementation, you would get these details from the payment provider
            new_method = PaymentMethod.objects.create(
                user=request.user,
                provider_payment_method_id=payment_method_id,
                payment_provider='stripe',
                type='card',
                brand='visa',  # This would come from the payment provider
                last4='4242',  # This would come from the payment provider
                exp_month=12,  # This would come from the payment provider
                exp_year=2025,  # This would come from the payment provider
                is_default=set_default
            )

            # If this is set as default, unset any existing default
            if set_default:
                PaymentMethod.objects.filter(user=request.user, is_default=True).exclude(id=new_method.id).update(is_default=False)

            messages.success(request, "Payment method added successfully.")

        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error adding payment method: {str(e)}")
        messages.error(request, f"An error occurred while adding your payment method. Please try again.")
        return redirect('subscription:manage_subscription')


@login_required
@require_POST
def remove_payment_method(request, payment_method_id):
    """View for removing a payment method."""
    # Get payment method
    from .models import PaymentMethod
    payment_method = get_object_or_404(
        PaymentMethod,
        provider_payment_method_id=payment_method_id,
        user=request.user
    )

    try:
        # In a real implementation, you would use the payment provider's API to detach the payment method

        # Check if this is the default payment method
        was_default = payment_method.is_default

        # Delete the payment method
        payment_method.delete()

        # If this was the default, set another one as default
        if was_default:
            next_method = PaymentMethod.objects.filter(user=request.user).first()
            if next_method:
                next_method.is_default = True
                next_method.save()

        messages.success(request, "Payment method removed successfully.")

        # Return HTML for HTMX
        if request.headers.get('HX-Request'):
            return HttpResponse("")

        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error removing payment method: {str(e)}")
        messages.error(request, f"An error occurred while removing your payment method. Please try again.")

        # Return HTML for HTMX
        if request.headers.get('HX-Request'):
            return HttpResponse("Error removing payment method", status=500)

        return redirect('subscription:manage_subscription')


@login_required
@require_POST
def set_default_payment_method(request, payment_method_id):
    """View for setting a payment method as default."""
    # Get payment method
    from .models import PaymentMethod
    payment_method = get_object_or_404(
        PaymentMethod,
        provider_payment_method_id=payment_method_id,
        user=request.user
    )

    try:
        # In a real implementation, you would use the payment provider's API to set the default payment method

        # Unset any existing default
        PaymentMethod.objects.filter(user=request.user, is_default=True).update(is_default=False)

        # Set this one as default
        payment_method.is_default = True
        payment_method.save()

        messages.success(request, "Default payment method updated successfully.")

        # Return HTML for HTMX
        if request.headers.get('HX-Request'):
            return render(request, 'subscription/partials/payment_method.html', {'method': payment_method})

        return redirect('subscription:manage_subscription')

    except Exception as e:
        logger.exception(f"Error setting default payment method: {str(e)}")
        messages.error(request, f"An error occurred while updating your default payment method. Please try again.")

        # Return HTML for HTMX
        if request.headers.get('HX-Request'):
            return HttpResponse("Error setting default payment method", status=500)

        return redirect('subscription:manage_subscription')