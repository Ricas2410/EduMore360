"""
Validators for the quiz app.
This module contains validation logic for quiz answers.
"""

import re
import difflib

# Simple word tokenizer that doesn't require NLTK
def simple_tokenize(text):
    """Split text into words without using NLTK."""
    return re.findall(r'\b\w+\b', text.lower())

# Common English stop words
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
    'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
    'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
    'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
    'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
    'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
    'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
    'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now'
}


class ShortAnswerValidator:
    """Validator for short answer questions."""

    @staticmethod
    def normalize_text(text):
        """
        Normalize text for comparison:
        - Convert to lowercase
        - Remove punctuation
        - Remove extra whitespace
        - Lemmatize words (if NLTK is available)
        - Remove stop words (if NLTK is available)

        Args:
            text: The text to normalize

        Returns:
            Normalized text
        """
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove stop words using our simple tokenizer
        words = simple_tokenize(text)
        words = [word for word in words if word not in STOP_WORDS]
        text = ' '.join(words)

        return text

    @staticmethod
    def exact_match(student_answer, correct_answer):
        """
        Check if the student's answer exactly matches the correct answer.

        Args:
            student_answer: The student's answer
            correct_answer: The correct answer

        Returns:
            True if the answers match, False otherwise
        """
        return ShortAnswerValidator.normalize_text(student_answer) == ShortAnswerValidator.normalize_text(correct_answer)

    @staticmethod
    def fuzzy_match(student_answer, correct_answer, threshold=0.8):
        """
        Check if the student's answer is similar to the correct answer using fuzzy matching.

        Args:
            student_answer: The student's answer
            correct_answer: The correct answer
            threshold: The similarity threshold (0.0 to 1.0)

        Returns:
            True if the similarity is above the threshold, False otherwise
        """
        # Normalize both answers
        norm_student = ShortAnswerValidator.normalize_text(student_answer)
        norm_correct = ShortAnswerValidator.normalize_text(correct_answer)

        # If either is empty after normalization, return False
        if not norm_student or not norm_correct:
            return False

        # Calculate similarity ratio
        similarity = difflib.SequenceMatcher(None, norm_student, norm_correct).ratio()

        return similarity >= threshold

    @staticmethod
    def contains_keywords(student_answer, keywords, threshold=0.7):
        """
        Check if the student's answer contains the required keywords.

        Args:
            student_answer: The student's answer
            keywords: List of required keywords
            threshold: The proportion of keywords that must be present

        Returns:
            True if enough keywords are present, False otherwise
        """
        if not keywords:
            return False

        # Normalize student answer
        norm_student = ShortAnswerValidator.normalize_text(student_answer)

        # Count how many keywords are in the student's answer
        matches = 0
        for keyword in keywords:
            norm_keyword = ShortAnswerValidator.normalize_text(keyword)
            if norm_keyword in norm_student:
                matches += 1

        # Calculate the proportion of keywords that matched
        match_ratio = matches / len(keywords)

        return match_ratio >= threshold

    @staticmethod
    def validate_answer(student_answer, correct_answers):
        """
        Validate a student's answer against a list of correct answers.

        Args:
            student_answer: The student's answer
            correct_answers: List of ShortAnswer objects

        Returns:
            True if the answer is correct, False otherwise
        """
        for answer in correct_answers:
            if answer.is_exact_match:
                # For exact match answers, use exact matching
                if ShortAnswerValidator.exact_match(student_answer, answer.text):
                    return True
            else:
                # For fuzzy match answers, use fuzzy matching
                if ShortAnswerValidator.fuzzy_match(student_answer, answer.text):
                    return True

                # Also check for keywords if the answer contains commas (indicating a list of keywords)
                if ',' in answer.text:
                    keywords = [k.strip() for k in answer.text.split(',')]
                    if ShortAnswerValidator.contains_keywords(student_answer, keywords):
                        return True

        return False
