-- Add topics if they don't exist
INSERT INTO curriculum_topic (name, description, slug, order, is_active, subject_id, created_at, updated_at)
SELECT 'Addition and Subtraction', 'Addition and subtraction of numbers up to 1000', 'addition-and-subtraction', 1, 1, s.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_subject s
JOIN curriculum_classlevel cl ON s.class_level_id = cl.id
JOIN curriculum_curriculum c ON cl.curriculum_id = c.id
WHERE c.code = 'US' AND cl.name = 'Grade 3' AND s.name = 'Mathematics'
AND NOT EXISTS (
    SELECT 1 FROM curriculum_topic t
    WHERE t.subject_id = s.id AND t.name = 'Addition and Subtraction'
);

INSERT INTO curriculum_topic (name, description, slug, order, is_active, subject_id, created_at, updated_at)
SELECT 'Living Things', 'Study of plants and animals', 'living-things', 1, 1, s.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_subject s
JOIN curriculum_classlevel cl ON s.class_level_id = cl.id
JOIN curriculum_curriculum c ON cl.curriculum_id = c.id
WHERE c.code = 'GH' AND cl.name = 'Primary 4' AND s.name = 'Science'
AND NOT EXISTS (
    SELECT 1 FROM curriculum_topic t
    WHERE t.subject_id = s.id AND t.name = 'Living Things'
);

-- US Curriculum - Grade 5 - English - Noun - Multiple Choice Questions
INSERT INTO quiz_question (text, question_type, difficulty, explanation, is_active, is_premium, curriculum_id, class_level_id, subject_id, topic_id, created_at, updated_at)
SELECT 'Which of the following is a proper noun?', 'multiple_choice', 'medium',
       'Proper nouns are specific names of people, places, or things and are always capitalized.',
       1, 0, c.id, cl.id, s.id, t.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun';

-- Get the ID of the question we just inserted
-- Using SQLite's last_insert_rowid() function
-- This will be handled in the Python script

-- Insert choices for the first noun question
INSERT INTO quiz_questionchoice (question_id, text, is_correct)
VALUES
(@noun_q1_id, 'New York', 1),
(@noun_q1_id, 'city', 0),
(@noun_q1_id, 'book', 0),
(@noun_q1_id, 'teacher', 0);

-- Second noun question
INSERT INTO quiz_question (text, question_type, difficulty, explanation, is_active, is_premium, curriculum_id, class_level_id, subject_id, topic_id, created_at, updated_at)
SELECT 'Which sentence contains a collective noun?', 'multiple_choice', 'medium',
       'Collective nouns refer to groups of people or things, such as "team," "family," "flock," etc.',
       1, 0, c.id, cl.id, s.id, t.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun';

-- Get the ID of the question we just inserted
-- Using SQLite's last_insert_rowid() function
-- This will be handled in the Python script

-- Insert choices for the second noun question
INSERT INTO quiz_questionchoice (question_id, text, is_correct)
VALUES
(@noun_q2_id, 'The team won the championship.', 1),
(@noun_q2_id, 'She bought a new car.', 0),
(@noun_q2_id, 'The dog barked loudly.', 0),
(@noun_q2_id, 'He wrote a letter.', 0);

-- Third noun question
INSERT INTO quiz_question (text, question_type, difficulty, explanation, is_active, is_premium, curriculum_id, class_level_id, subject_id, topic_id, created_at, updated_at)
SELECT 'Which of the following is an abstract noun?', 'multiple_choice', 'medium',
       'Abstract nouns represent ideas, qualities, or states that cannot be seen or touched, such as "happiness," "love," "courage," etc.',
       1, 0, c.id, cl.id, s.id, t.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun';

-- Get the ID of the question we just inserted
-- Using SQLite's last_insert_rowid() function
-- This will be handled in the Python script

-- Insert choices for the third noun question
INSERT INTO quiz_questionchoice (question_id, text, is_correct)
VALUES
(@noun_q3_id, 'Happiness', 1),
(@noun_q3_id, 'Table', 0),
(@noun_q3_id, 'Dog', 0),
(@noun_q3_id, 'Mountain', 0);

-- US Curriculum - Grade 5 - English - Noun - Short Answer Questions
INSERT INTO quiz_question (text, question_type, difficulty, explanation, is_active, is_premium, curriculum_id, class_level_id, subject_id, topic_id, created_at, updated_at)
SELECT 'Write a proper noun for a famous city.', 'short_answer', 'medium',
       'Proper nouns are specific names of people, places, or things and are always capitalized.',
       1, 0, c.id, cl.id, s.id, t.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun';

-- Get the ID of the question we just inserted
-- Using SQLite's last_insert_rowid() function
-- This will be handled in the Python script

-- Insert answers for the first short answer question
INSERT INTO quiz_shortanswer (question_id, text)
VALUES
(@noun_sa1_id, 'New York'),
(@noun_sa1_id, 'London'),
(@noun_sa1_id, 'Paris'),
(@noun_sa1_id, 'Tokyo'),
(@noun_sa1_id, 'Beijing'),
(@noun_sa1_id, 'Rome'),
(@noun_sa1_id, 'Cairo'),
(@noun_sa1_id, 'Sydney');

-- Second short answer question
INSERT INTO quiz_question (text, question_type, difficulty, explanation, is_active, is_premium, curriculum_id, class_level_id, subject_id, topic_id, created_at, updated_at)
SELECT 'What is a collective noun for a group of lions?', 'short_answer', 'medium',
       'A group of lions is called a "pride."',
       1, 0, c.id, cl.id, s.id, t.id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun';

-- Get the ID of the question we just inserted
-- Using SQLite's last_insert_rowid() function
-- This will be handled in the Python script

-- Insert answer for the second short answer question
INSERT INTO quiz_shortanswer (question_id, text)
VALUES
(@noun_sa2_id, 'pride');

-- Create a quiz for the Noun topic
INSERT INTO quiz_quiz (title, description, quiz_type, question_count, time_limit, per_question_time, randomize_questions, randomize_choices, show_immediate_feedback, passing_score, is_active, is_featured, curriculum_id, class_level_id, subject_id, topic_id, created_by_id, created_at, updated_at)
SELECT 'Nouns Quiz', 'Test your knowledge of nouns', 'topic', 5, 0, 30, 1, 1, 1, 70, 1, 0, c.id, cl.id, s.id, t.id, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM curriculum_curriculum c
JOIN curriculum_classlevel cl ON cl.curriculum_id = c.id
JOIN curriculum_subject s ON s.curriculum_id = c.id AND s.class_level_id = cl.id
JOIN curriculum_topic t ON t.subject_id = s.id
WHERE c.code = 'US' AND cl.name = 'Grade 5' AND s.name = 'English' AND t.name = 'Noun'
AND NOT EXISTS (
    SELECT 1 FROM quiz_quiz q
    WHERE q.curriculum_id = c.id AND q.class_level_id = cl.id AND q.subject_id = s.id AND q.topic_id = t.id AND q.title = 'Nouns Quiz'
);
