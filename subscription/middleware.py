import re
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import Subscription, SubscriptionPlan, CurriculumAccess
from curriculum.models import Curriculum, ClassLevel, Note

class SubscriptionMiddleware:
    """
    Middleware to enforce subscription restrictions.

    This middleware checks if a user has an active subscription for premium content.
    If not, they are redirected to the subscription plans page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Paths that require an active subscription
        self.premium_paths = [
            r'^/curriculum/notes/\d+/$',  # Individual note view
            r'^/curriculum/lessons/\d+/$',  # Individual lesson view
            r'^/quiz/take/\d+/$',  # Take quiz
            r'^/quiz/create/$',  # Create quiz
        ]

        # Paths that require subscription tier access check
        self.curriculum_paths = [
            r'^/curriculum/([^/]+)/(\d+)/',  # Curriculum with class level
            r'^/curriculum/([^/]+)/(\d+)/([^/]+)/',  # Subject detail
            r'^/curriculum/([^/]+)/(\d+)/([^/]+)/([^/]+)/',  # Branch or topic detail
            r'^/curriculum/([^/]+)/(\d+)/([^/]+)/([^/]+)/([^/]+)/',  # Subtopic detail
        ]

        # Paths that are always allowed
        self.allowed_paths = [
            r'^/admin/',
            r'^/accounts/',
            r'^/subscription/',
            r'^/static/',
            r'^/media/',
            r'^/$',  # Home page
            r'^/about/$',
            r'^/contact/$',
            r'^/curriculum/$',  # Curriculum index
            r'^/curriculum/subjects/$',  # Subject list
            r'^/quiz/$',  # Quiz index
            r'^/quiz/categories/$',  # Quiz categories
        ]

    def __call__(self, request):
        # Skip middleware for non-authenticated users
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip middleware for staff/admin users
        if request.user.is_staff or request.user.is_superuser:
            return self.get_response(request)

        # Check if the path requires a subscription
        path = request.path

        # Always allow certain paths
        for pattern in self.allowed_paths:
            if re.match(pattern, path):
                return self.get_response(request)

        # Get active subscription if user is authenticated
        active_subscription = None
        if request.user.is_authenticated:
            active_subscription = Subscription.objects.filter(
                user=request.user,
                status='active',
                end_date__gt=timezone.now()
            ).first()

        # Check if the path is for curriculum navigation
        curriculum_access_check = False
        curriculum_code = None
        class_level_id = None

        for pattern in self.curriculum_paths:
            match = re.match(pattern, path)
            if match:
                curriculum_access_check = True
                curriculum_code = match.group(1)
                class_level_id = match.group(2)
                break

        if curriculum_access_check and curriculum_code and class_level_id:
            # Get the curriculum and class level objects
            curriculum = Curriculum.objects.filter(code=curriculum_code).first()
            class_level = ClassLevel.objects.filter(id=class_level_id).first()

            if curriculum and class_level:
                # If no active subscription, only allow access to free tier content
                if not active_subscription:
                    # Get the free tier sample curriculum and class level
                    free_curriculum = None
                    free_class_level = None

                    # Find a free subscription to determine what's available in free tier
                    free_plan = SubscriptionPlan.objects.filter(plan_type='free').first()
                    if free_plan:
                        # Find a sample curriculum access for the free tier
                        sample_access = CurriculumAccess.objects.filter(
                            subscription__plan=free_plan
                        ).first()

                        if sample_access:
                            free_curriculum = sample_access.curriculum
                            free_class_level = sample_access.class_level

                    # If this is not the free tier content, redirect
                    if not (free_curriculum and free_class_level and
                            free_curriculum.id == curriculum.id and
                            free_class_level.id == class_level.id):
                        message = f"Access to {curriculum.name} - {class_level.name} requires a subscription. Please subscribe to access this content."
                        return redirect(reverse('subscription:access_denied') +
                                       f"?curriculum_id={curriculum.id}&class_level_id={class_level.id}&message={message}")

                # If has subscription, check if it allows access to this curriculum and class level
                elif not active_subscription.has_access_to_class_level(curriculum, class_level):
                    message = f"Your current subscription plan does not include access to {curriculum.name} - {class_level.name}. Please upgrade your subscription to access this content."
                    return redirect(reverse('subscription:access_denied') +
                                   f"?curriculum_id={curriculum.id}&class_level_id={class_level.id}&message={message}")

        # Check if the path is premium content
        requires_subscription = False
        for pattern in self.premium_paths:
            if re.match(pattern, path):
                requires_subscription = True
                break

        if requires_subscription:
            # Check if user has an active subscription
            if not active_subscription:
                messages.warning(
                    request,
                    "This content requires an active subscription. Please subscribe to access premium content."
                )
                return redirect(reverse('subscription:subscription_plans'))

            # Check for specific note access
            note_id_match = re.search(r'/curriculum/notes/(\d+)/', path)
            if note_id_match:
                # Extract note ID from URL
                note_id = note_id_match.group(1)

                # Get the note object
                note = Note.objects.filter(id=note_id).first()

                if note:
                    # Get the curriculum and class level from the note
                    curriculum = note.topic.subject.curriculum
                    class_level = note.topic.subject.class_level

                    # Check if the user's subscription allows access to this note
                    if not active_subscription.has_access_to_content(note):
                        message = f"Your current subscription plan does not include access to content from {curriculum.name} - {class_level.name}. Please upgrade your subscription to access this content."
                        return redirect(reverse('subscription:access_denied') +
                                       f"?curriculum_id={curriculum.id}&class_level_id={class_level.id}&message={message}")

        return self.get_response(request)
