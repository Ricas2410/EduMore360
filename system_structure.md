## 📘 Educational System Flow & Structure

### 🔖 Question Bank Structure

Organize all educational content using this hierarchical structure:

```
Country (Curriculum) > Class Level > Subject > Branch (if applicable) > Topic > Sub-topic (if any)
```

- **Each quiz question** should be linked to:
  - Curriculum (Country)
  - Class Level
  - Subject
  - Topic / Sub-topic
  - **Correct Answer**
  - **Explanation** *(newly required: brief clarification for incorrect answers)*

- **Each note** should also follow the same structure and be stored under its specific topic/sub-topic.

---

### 🧭 User Navigation Flow

When a student accesses the system, the flow should be:

1. **Select Curriculum** (e.g., Ghana, US)
2. **Select Class Level** (e.g., SHS 1, Grade 8)
3. **Select Subject** (e.g., Science, English)
4. Choose between:

   #### 📒 Notes
   - If applicable, select a **Branch** (e.g., Biology, Chemistry)
   - Select **Topic > Sub-topic** (if available)
   - View the note content

   #### 🧪 Quiz
   - Option 1: **General Quiz** – All questions under the subject
   - Option 2: **Topic-Based Quiz** – Only questions for selected topic
   - Quiz Questions should include:
     - Question text
     - Options (multiple choice)
     - Correct answer
     - **Explanation** (displayed if the user gets the answer wrong)

---

### ✅ Feedback Mechanism (Quiz Interaction)

For each quiz attempt:

- If the student selects the **correct answer**:
  - Display: ✅ *Correct* with proper animation (next question loads)

- If the student selects the **wrong answer**:
  - Display: ❌ *Incorrect*
  - Show the **Correct Answer**
  - Show the **Explanation**, e.g.,  
    *"Your approach is incorrect. The correct answer is C "Ruminant" because... [brief explanation]."*
continue button to load next question.
---

### 🔧 Required Developer Changes

- Implement or update database models to store:
  - Country (as Curriculum)
  - Class Level
  - Subject
  - Branch (optional)
  - Topic & Sub-topic
  - Question + Correct Answer + **Explanation**
  - Notes content linked similarly

- Update both **Admin Panel** and **Frontend** to follow this structure strictly.

- Make the quiz engine capable of:
  - General and topic-based question loading
  - Displaying real-time feedback with explanations
  - Navigating using the correct hierarchy


Also: Add the following if not already implemented
Gamification:

Add elements like badges, leaderboards, and rewards to motivate students and enhance engagement.
Search Functionality:
Include a robust search feature that allows students to find specific questions, notes, or topics easily.
Feedback and Reporting:
Enable students to provide feedback on questions and notes, which can help improve content quality.
Multimedia Content:
Allow the inclusion of images, videos, and audio in notes and quizzes to cater to different learning styles.