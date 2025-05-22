#!/usr/bin/env python
"""
Script to check ICT topics for Primary 6.
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings')
django.setup()

from curriculum.models import Subject, Topic


def check_ict_topics():
    """Check ICT topics for Primary 6."""
    try:
        ict_subject = Subject.objects.get(name='ICT', class_level__name='Primary 6')
        print(f"ICT Subject found: {ict_subject.name} - {ict_subject.class_level.name}")
        
        topics = ict_subject.topics.all()
        print(f"\nICT Topics for Primary 6 ({topics.count()} topics):")
        for topic in topics:
            print(f"- {topic.name}")
            print(f"  Description: {topic.description}")
            print(f"  Questions: {topic.questions.count()}")
            print()
            
    except Subject.DoesNotExist:
        print("ICT subject for Primary 6 not found!")


if __name__ == "__main__":
    check_ict_topics()
