#!/usr/bin/env python
"""
Script to create subscription plans for EduMore360.
This script can be run directly or imported and used in other scripts.
"""

import os
import sys
import django
from decimal import Decimal

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from subscription.models import SubscriptionPlan


def create_subscription_plans():
    """Create subscription plans for the application."""
    print('Creating subscription plans...')
    
    # Define plan features
    free_features = (
        "Access to one curriculum and one grade level\n"
        "Limited quiz attempts (5 per day)\n"
        "Basic progress tracking\n"
        "Ad-supported experience\n"
        "Email support"
    )
    
    tier_one_features = (
        "Access to one curriculum and all grade levels\n"
        "Unlimited quiz attempts\n"
        "Detailed progress tracking\n"
        "Ad-free experience\n"
        "Email and chat support\n"
        "Download study materials\n"
        "Access to practice exams"
    )
    
    tier_two_features = (
        "Access to all curriculums and all grade levels\n"
        "Unlimited quiz attempts\n"
        "Advanced progress tracking and analytics\n"
        "Ad-free experience\n"
        "Priority email and chat support\n"
        "Download all study materials\n"
        "Access to all practice exams\n"
        "Personalized study plans\n"
        "Offline access to content"
    )
    
    tier_three_features = (
        "Access to all curriculums and all grade levels\n"
        "Unlimited quiz attempts\n"
        "Advanced progress tracking and analytics\n"
        "Ad-free experience\n"
        "Priority email, chat, and phone support\n"
        "Download all study materials\n"
        "Access to all practice exams\n"
        "Personalized study plans\n"
        "Offline access to content\n"
        "Family account with up to 5 users\n"
        "Dedicated account manager\n"
        "Early access to new features"
    )
    
    # Define plan prices
    tier_one_monthly_price = Decimal('9.99')
    tier_two_monthly_price = Decimal('19.99')
    tier_three_monthly_price = Decimal('39.99')
    
    # Calculate yearly prices with 10% discount
    discount = Decimal('0.9')  # 10% discount
    tier_one_yearly_price = (tier_one_monthly_price * 12 * discount).quantize(Decimal('0.01'))
    tier_two_yearly_price = (tier_two_monthly_price * 12 * discount).quantize(Decimal('0.01'))
    tier_three_yearly_price = (tier_three_monthly_price * 12 * discount).quantize(Decimal('0.01'))
    
    # Create plans
    plans = [
        # Free tier
        {
            'name': 'Free Tier',
            'plan_type': 'free',
            'description': 'Basic access to educational content with limited features.',
            'price': Decimal('0.00'),
            'billing_cycle': 'monthly',
            'features': free_features,
            'max_users': 1,
            'all_curriculums': False,
            'all_grade_levels': False,
        },
        
        # Tier One - Monthly
        {
            'name': 'Standard Plan - Monthly',
            'plan_type': 'tier_one',
            'description': 'Enhanced access to educational content with more features.',
            'price': tier_one_monthly_price,
            'billing_cycle': 'monthly',
            'features': tier_one_features,
            'max_users': 1,
            'all_curriculums': False,
            'all_grade_levels': True,
        },
        
        # Tier One - Yearly
        {
            'name': 'Standard Plan - Yearly',
            'plan_type': 'tier_one',
            'description': 'Enhanced access to educational content with more features. Save 10% with yearly billing.',
            'price': tier_one_yearly_price,
            'billing_cycle': 'yearly',
            'features': tier_one_features,
            'max_users': 1,
            'all_curriculums': False,
            'all_grade_levels': True,
        },
        
        # Tier Two - Monthly
        {
            'name': 'Premium Plan - Monthly',
            'plan_type': 'tier_two',
            'description': 'Full access to all educational content and premium features.',
            'price': tier_two_monthly_price,
            'billing_cycle': 'monthly',
            'features': tier_two_features,
            'max_users': 1,
            'all_curriculums': True,
            'all_grade_levels': True,
        },
        
        # Tier Two - Yearly
        {
            'name': 'Premium Plan - Yearly',
            'plan_type': 'tier_two',
            'description': 'Full access to all educational content and premium features. Save 10% with yearly billing.',
            'price': tier_two_yearly_price,
            'billing_cycle': 'yearly',
            'features': tier_two_features,
            'max_users': 1,
            'all_curriculums': True,
            'all_grade_levels': True,
        },
        
        # Tier Three - Monthly
        {
            'name': 'Family Plan - Monthly',
            'plan_type': 'tier_three',
            'description': 'Complete access to all content and features for the whole family.',
            'price': tier_three_monthly_price,
            'billing_cycle': 'monthly',
            'features': tier_three_features,
            'max_users': 5,
            'all_curriculums': True,
            'all_grade_levels': True,
        },
        
        # Tier Three - Yearly
        {
            'name': 'Family Plan - Yearly',
            'plan_type': 'tier_three',
            'description': 'Complete access to all content and features for the whole family. Save 10% with yearly billing.',
            'price': tier_three_yearly_price,
            'billing_cycle': 'yearly',
            'features': tier_three_features,
            'max_users': 5,
            'all_curriculums': True,
            'all_grade_levels': True,
        },
    ]
    
    # Create or update plans
    for plan_data in plans:
        plan, created = SubscriptionPlan.objects.update_or_create(
            plan_type=plan_data['plan_type'],
            billing_cycle=plan_data['billing_cycle'],
            defaults=plan_data
        )
        
        if created:
            print(f'Created plan: {plan.name}')
        else:
            print(f'Updated plan: {plan.name}')
    
    print('Subscription plans created successfully!')


if __name__ == '__main__':
    create_subscription_plans()
