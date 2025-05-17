# Edumore360 - Educational Platform Overview

## Introduction

Edumore360 is a comprehensive educational platform designed to support students from kindergarten through grade 12. The platform provides a rich repository of educational content, including notes and questions, organized by grade level, subject, and topic. The system aims to enhance learning through interactive question-answering sessions and detailed notes on various subjects, with a focus on US and Ghana curriculum standards.

## Core Features

### 👤 User Types and Management

1. **Admin**
   - Full access to manage:
     - Users and their permissions
     - Content (notes, questions, media)
     - Curriculum structures and alignments
     - Subscription tiers and pricing
     - Site configurations and settings
   - Comprehensive dashboard for:
     - Analytics (user activity, most-read topics, performance metrics)
     - Content creation and editing tools
     - Moderation and approval workflows
     - System health monitoring

2. **User Subscription Tiers**
   - **Freemium**
     - Limited access ()
     - Ad-supported experience
     - Basic progress tracking
     - Limited question attempts

   - **Pro**
     - Full access to all grades and subjects
     - Ad-free experience
     - Comprehensive analytics and progress tracking
     - Unlimited question attempts
     - Downloadable content

   - **Family**
     - One primary paying account
     - Can add up to 5 sub-users (e.g., children)
     - All sub-users receive Pro-level access
     - Family progress dashboard for parents
     - Shared payment method

   - **Enterprise**
     - For schools and educational organizations
     - Unlimited user additions
     - Bulk user management
     - Custom branding options
     - Advanced analytics for administrators
     - API access for integration with school systems

3. **User Dashboard**
   - Personalized based on user type and subscription level
   quick links to key features (include quize page and learn page)
   - Progress tracking across subjects and topics
   - Recent activity timeline
   - Recommended content based on learning patterns
   - Achievement badges and gamification elements

### 📚 Content Structure and Management

1. **Subject & Curriculum Mapping**
   - Subjects and topics grouped by:
     - Grade level (K-12)
     - Curriculum standard (US, Ghana, etc.)
   - Curriculum switcher in UI for easy navigation
   - Cross-referencing between equivalent topics in different curricula
   - Difficulty levels within each topic

2. **Notes/Lessons Repository**
   - Rich text-based notes for each topic
   - Support for:
     - Embedded YouTube/Vimeo video lessons
     - Interactive diagrams and illustrations
     - PDF attachments for printable content
     - Mathematical equations and formulas
   - Pre-quiz study materials
   - Searchable content with keyword indexing

3. **Question Bank**
   - Multiple formats:
     - Multiple-choice questions (MCQs)
     - Short-answer questions with auto-grading
   - Questions tagged by:
     - Subject and topic
     - Grade level
     - Difficulty level
     - Curriculum alignment
   - Randomized delivery system to prevent repetition
   - Detailed explanations for both correct and incorrect answers
   - Retry mode with new question variations

### 🎓 Learning Experience

1. **Study Mode**
   - Structured learning paths through topics
   - Bookmarking and note-taking capabilities
   - Progress tracking with completion indicators
   - Spaced repetition suggestions for review
   - Offline access to downloaded content (Pro and above)

2. **Quizzing System**
   - Configurable timer options
   - Instant feedback on answers
   - Scoring and performance metrics
   - "Try again" and "See explanation" options
   - Review mode for completed quizzes
   - Performance history and improvement tracking


### ⚙️ Admin Functionality

1. **System Configuration**
   - Email SMTP setup and configuration
   - Session management controls (single session toggle)
   - Curriculum management and organization
   - Subject and topic structure configuration
   - Subscription tier management and pricing
   - Notification system settings and templates
   - Site-wide settings and preferences

### 🔄 System Workflows

1. **Content Management**
   - Streamlined content creation workflow:
     - Draft creation and editing
     - Review and approval process
     - Publishing and versioning
     - Bulk import/export capabilities
   - Media management system:
     - Image optimization
     - Video embedding from multiple sources
     - File attachment handling
   - Content organization tools:
     - Tagging and categorization
     - Relationship mapping between topics
     - Prerequisite linking

2. **User Management**
   - Registration and onboarding:
     - Email verification
     - Profile completion guidance
     - Initial assessment for level placement
   - Subscription handling:
     - Payment processing (Paystack integration)
     - Subscription lifecycle management
     - Upgrade/downgrade pathways
     - Family/Enterprise user invitation system
   - Access control:
     - Role-based permissions
     - Content access restrictions by subscription
     - IP-based security measures
     - Single session enforcement (configurable by admin)
     - Secure authentication for all users (including those added by Family/Enterprise accounts)

3. **Notification System**
   - User notifications:
     - Email notifications (using admin-configured SMTP)
     - In-app notifications
     - Push notifications (for mobile users)
     - Subscription status alerts
   - Admin notifications:
     - New user registrations
     - Payment events
     - System performance alerts
     - Content approval requests


## User Journeys

### Student Journey

1. **Registration and Onboarding**
   - Sign up with email or social login
   - Select grade level and curriculum preference
   - Choose subscription tier or start with free access
   - Complete profile with learning preferences
   - Take optional placement assessment

2. **Content Discovery**
   - Browse subjects and topics by grade level
   - Use search functionality with filters
   - View personalized recommendations
   - Explore trending or popular content
   - Follow structured learning paths

3. **Learning Process**
   - Select a topic of interest
   - Review comprehensive notes and lessons
   - Watch embedded video content if available
   - Take practice quizzes with immediate feedback
   - Review explanations for incorrect answers
   - Track progress through topic completion indicators

4. **Assessment and Progress**
   - Complete timed or untimed quizzes
   - Receive detailed performance feedback
   - Identify areas for improvement
   - Review incorrect answers with explanations
   - Track progress across subjects and topics
   - Earn achievements and completion badges

5. **Subscription Management**
   - Upgrade subscription for additional features
   - Add family members (Family plan) with secure authentication
   - Manage payment methods and billing
   - View subscription history and receipts
   - Receive notifications about subscription status

### Admin Journey

1. **Content Creation and Management**
   - Create curriculum structures aligned to standards
   - Organize subjects and topics in hierarchical structure
   - Create rich text notes with embedded media
   - Develop question banks with varied formats
   - Link questions to appropriate topics and difficulty levels
   - Review and approve content from other admins

2. **User and Subscription Administration**
   - Review new user registrations
   - Configure subscription tiers and pricing
   - Manage enterprise accounts and bulk users
   - Handle user support requests and issues
   - Monitor user activity and engagement metrics

### 🖥️ Technology Stack

1. **Frontend**
   - **Framework**: Django Templates as the base
   - **CSS Framework**: Tailwind CSS for responsive styling
   - **Component Library**: DaisyUI for pre-built UI components
   - **Interactivity**:
     - HTMX for dynamic content loading without full page refreshes
     - Alpine.js for client-side interactivity and state management
   - **Responsive Design**: Mobile-first approach ensuring compatibility across all devices

2. **Backend**
   - **Framework**: Django 5.x for robust application structure
   - **Database**: PostgreSQL for relational data storage
   - **Caching**: Redis for performance optimization
   - **Async Tasks**: Celery with Redis as broker for background processing
   - **API**: Django REST Framework for potential mobile app integration

3. **Infrastructure**
   - **Deployment**: Docker containerization
   - **Media Storage**: Cloud storage for user uploads and media
   - **CDN**: For static asset delivery
   - **Monitoring**: Application performance monitoring
   - **Backup**: Automated database backup system

3. **Question Engine**
   - Sophisticated randomization algorithm
   - Answer validation with fuzzy matching for short answers
   - Performance tracking and analytics
   - Feedback generation with explanations
   - Difficulty adjustment based on user performance

4. **Subscription Management**
   - Paystack integration for payments
   - Subscription lifecycle handling
   - Multi-user management for Family/Enterprise
   - Proration and upgrade/downgrade logic
   - Payment history and receipts

5. **Notification Engine**
   - Email notification system with admin-configurable SMTP
   - In-app notification center
   - Push notification capability
   - Notification preferences management
   - Templated notification messages

### 📊 Data Models

1. **User-Related Models**
   - **User**
     - Basic information (name, email, etc.)
     - Authentication details
     - Profile settings and preferences
     - Learning history and preferences

   - **Subscription**
     - Type (Free, Pro, Enterprise, Family)
     - Payment information and history
     - Start and end dates
     - Status tracking
     - Related users (for Family/Enterprise)
(can choose to pay yearly)

   - **UserGroup**
     - For Family/Enterprise subscriptions
     - Group administrator
     - Member management (limited to 5 for Family, unlimited for Enterprise)
     - Group settings and permissions

2. **Content-Related Models**
   - **Curriculum**
     - Standard type (US, Ghana)
     - Grade level ranges
     - Subject organization

   - **Subject**
     - Name and description
     - Grade level association
     - Curriculum alignment
     - Learning objectives

   - **Topic**
     - Name and description
     - Parent subject relationship
     - Difficulty level
     - Prerequisites
     - Learning outcomes

   - **Note/Lesson**
     - Title and content (rich text)
     - Topic association
     - Media attachments
     - Author and timestamps
     - Version history

   - **Question**
     - Question text and format
     - Answer options (for MCQs)
     - Correct answer(s)
     - Explanation content
     - Difficulty rating
     - Topic association
     - Usage statistics

3. **Progress-Related Models**
   - **UserProgress**
     - User reference
     - Topic/subject tracking
     - Completion status
     - Performance metrics
     - Timestamp data

   - **QuizAttempt**
     - User reference
     - Questions included
     - Answers provided
     - Score and analysis
     - Time taken
     - Feedback generated

4. **System-Related Models**
   - **SystemConfiguration**
     - SMTP server settings
     - Session management settings
     - Default notification templates
     - Site-wide preferences

   - **Notification**
     - User reference
     - Type and category
     - Content and metadata
     - Read/unread status
     - Timestamp information

## 🔒 Security and Compliance
  - Backup and disaster recovery procedures

## 📱 Multi-Platform Support

- **Responsive Web Design**
  - Mobile-first approach
  - Tablet optimization
  - Desktop enhancement
  - Touch-friendly interface elements

default email config:
SMTP Host: smtp.gmail.com
SMTP Port: 587
TLS: Enable
SMTP Username: skillnetservices@gmail.com
SMTP Password: tdms ckdk tmgo fado
Email Settings: skillnetservices@gmail.com
