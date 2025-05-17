"""
Patch to fix the question import functionality.

This patch modifies the duplicate detection logic in the import_questions function
to allow importing questions with the same text but different attributes.

To apply this patch:
1. Make a backup of your quiz/admin_views.py file
2. Find the section in import_questions where it checks for duplicate questions
3. Replace it with the code provided in this patch
"""

# Original code:
"""
# Check if a similar question already exists
existing_question = Question.objects.filter(
    text=question_text,
    question_type=question_type,
    curriculum=curriculum,
    class_level=class_level,
    subject=subject,
    topic=topic
).first()

if existing_question:
    errors.append(f"Row {row_num}: Question already exists (ID: {existing_question.id})")
    questions_skipped += 1
    continue
"""

# New code (replace the above section with this):
"""
# Check if a similar question already exists
existing_question = Question.objects.filter(
    text=question_text,
    question_type=question_type,
    curriculum=curriculum,
    class_level=class_level,
    subject=subject,
    topic=topic
).first()

if existing_question:
    # Check if we're trying to update the question with different attributes
    is_premium_different = existing_question.is_premium != is_premium
    is_active_different = existing_question.is_active != is_active
    difficulty_different = existing_question.difficulty != difficulty
    explanation_different = existing_question.explanation != explanation
    
    # If any attribute is different, update the existing question instead of skipping
    if is_premium_different or is_active_different or difficulty_different or explanation_different:
        # Update the existing question with the new attributes
        existing_question.is_premium = is_premium
        existing_question.is_active = is_active
        existing_question.difficulty = difficulty
        existing_question.explanation = explanation
        existing_question.save()
        
        # Log the update
        logger.info(f"Updated existing question (ID: {existing_question.id}) with new attributes")
        messages.info(request, f"Updated question (ID: {existing_question.id}) with new attributes")
        questions_created += 1
        new_question_ids.append(existing_question.id)
        continue
    else:
        # If no attributes are different, skip as a duplicate
        errors.append(f"Row {row_num}: Question already exists (ID: {existing_question.id})")
        questions_skipped += 1
        continue
"""
