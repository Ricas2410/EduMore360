/**
 * EduMore360 Quiz Functionality
 * 
 * This file contains the JavaScript functionality for the quiz feature.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Quiz timer functionality
    initQuizTimer();
    
    // Quiz navigation
    initQuizNavigation();
    
    // Quiz answer selection
    initQuizAnswerSelection();
    
    // Quiz submission
    initQuizSubmission();
});

/**
 * Initialize the quiz timer
 */
function initQuizTimer() {
    const timerElement = document.getElementById('quiz-timer');
    if (!timerElement) return;
    
    const quizTimeLimit = parseInt(timerElement.dataset.timeLimit || 0, 10);
    const quizId = timerElement.dataset.quizId;
    const attemptId = timerElement.dataset.attemptId;
    
    if (!quizTimeLimit || !quizId || !attemptId) return;
    
    let timeRemaining = parseInt(timerElement.dataset.timeRemaining || quizTimeLimit * 60, 10);
    let timerInterval;
    
    // Update the timer display
    function updateTimerDisplay() {
        const minutes = Math.floor(timeRemaining / 60);
        const seconds = timeRemaining % 60;
        
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // Update the timer color based on time remaining
        if (timeRemaining <= 60) { // Last minute
            timerElement.classList.add('text-error');
            timerElement.classList.add('animate-pulse');
        } else if (timeRemaining <= 300) { // Last 5 minutes
            timerElement.classList.add('text-warning');
            timerElement.classList.remove('text-error', 'animate-pulse');
        } else {
            timerElement.classList.remove('text-warning', 'text-error', 'animate-pulse');
        }
    }
    
    // Start the timer
    function startTimer() {
        updateTimerDisplay();
        
        timerInterval = setInterval(function() {
            timeRemaining--;
            updateTimerDisplay();
            
            // Save the time remaining to the server every 30 seconds
            if (timeRemaining % 30 === 0) {
                saveQuizProgress();
            }
            
            // Auto-submit when time is up
            if (timeRemaining <= 0) {
                clearInterval(timerInterval);
                document.getElementById('quiz-form').submit();
            }
        }, 1000);
    }
    
    // Save quiz progress to the server
    function saveQuizProgress() {
        const formData = new FormData();
        formData.append('quiz_id', quizId);
        formData.append('attempt_id', attemptId);
        formData.append('time_remaining', timeRemaining);
        
        // Get all selected answers
        const selectedAnswers = {};
        document.querySelectorAll('.quiz-question').forEach(question => {
            const questionId = question.dataset.questionId;
            const selectedOption = question.querySelector('input[type="radio"]:checked');
            
            if (selectedOption) {
                selectedAnswers[questionId] = selectedOption.value;
            }
        });
        
        formData.append('answers', JSON.stringify(selectedAnswers));
        
        fetch('/quiz/save-progress/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        }).catch(error => {
            console.error('Error saving quiz progress:', error);
        });
    }
    
    // Get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Start the timer
    startTimer();
    
    // Save progress when leaving the page
    window.addEventListener('beforeunload', function() {
        saveQuizProgress();
    });
}

/**
 * Initialize quiz navigation
 */
function initQuizNavigation() {
    const quizNavigation = document.getElementById('quiz-navigation');
    if (!quizNavigation) return;
    
    const questions = document.querySelectorAll('.quiz-question');
    const navButtons = document.querySelectorAll('.quiz-nav-button');
    
    // Show the first question by default
    if (questions.length > 0) {
        questions[0].classList.remove('hidden');
    }
    
    // Handle navigation button clicks
    navButtons.forEach(button => {
        button.addEventListener('click', function() {
            const questionIndex = parseInt(this.dataset.questionIndex, 10);
            
            // Hide all questions
            questions.forEach(question => {
                question.classList.add('hidden');
            });
            
            // Show the selected question
            if (questions[questionIndex]) {
                questions[questionIndex].classList.remove('hidden');
            }
            
            // Update active state of navigation buttons
            navButtons.forEach(btn => {
                btn.classList.remove('btn-active');
            });
            this.classList.add('btn-active');
            
            // Update progress indicator
            updateProgressIndicator(questionIndex + 1, questions.length);
        });
    });
    
    // Next and previous buttons
    const nextButton = document.getElementById('quiz-next-button');
    const prevButton = document.getElementById('quiz-prev-button');
    
    if (nextButton) {
        nextButton.addEventListener('click', function() {
            const currentQuestion = document.querySelector('.quiz-question:not(.hidden)');
            const currentIndex = Array.from(questions).indexOf(currentQuestion);
            const nextIndex = currentIndex + 1;
            
            if (nextIndex < questions.length) {
                // Hide current question
                currentQuestion.classList.add('hidden');
                
                // Show next question
                questions[nextIndex].classList.remove('hidden');
                
                // Update navigation buttons
                navButtons.forEach(btn => {
                    btn.classList.remove('btn-active');
                });
                
                if (navButtons[nextIndex]) {
                    navButtons[nextIndex].classList.add('btn-active');
                }
                
                // Update progress indicator
                updateProgressIndicator(nextIndex + 1, questions.length);
                
                // Enable/disable prev/next buttons
                prevButton.disabled = false;
                nextButton.disabled = nextIndex === questions.length - 1;
            }
        });
    }
    
    if (prevButton) {
        prevButton.addEventListener('click', function() {
            const currentQuestion = document.querySelector('.quiz-question:not(.hidden)');
            const currentIndex = Array.from(questions).indexOf(currentQuestion);
            const prevIndex = currentIndex - 1;
            
            if (prevIndex >= 0) {
                // Hide current question
                currentQuestion.classList.add('hidden');
                
                // Show previous question
                questions[prevIndex].classList.remove('hidden');
                
                // Update navigation buttons
                navButtons.forEach(btn => {
                    btn.classList.remove('btn-active');
                });
                
                if (navButtons[prevIndex]) {
                    navButtons[prevIndex].classList.add('btn-active');
                }
                
                // Update progress indicator
                updateProgressIndicator(prevIndex + 1, questions.length);
                
                // Enable/disable prev/next buttons
                prevButton.disabled = prevIndex === 0;
                nextButton.disabled = false;
            }
        });
        
        // Disable prev button initially
        prevButton.disabled = true;
    }
    
    // Update progress indicator
    function updateProgressIndicator(current, total) {
        const progressElement = document.getElementById('quiz-progress');
        if (progressElement) {
            progressElement.textContent = `Question ${current} of ${total}`;
            
            const progressBar = document.getElementById('quiz-progress-bar');
            if (progressBar) {
                const percentage = (current / total) * 100;
                progressBar.style.width = `${percentage}%`;
            }
        }
    }
    
    // Initialize progress indicator
    updateProgressIndicator(1, questions.length);
}

/**
 * Initialize quiz answer selection
 */
function initQuizAnswerSelection() {
    const quizForm = document.getElementById('quiz-form');
    if (!quizForm) return;
    
    const questions = document.querySelectorAll('.quiz-question');
    const navButtons = document.querySelectorAll('.quiz-nav-button');
    
    // Handle answer selection
    questions.forEach((question, index) => {
        const options = question.querySelectorAll('input[type="radio"]');
        const questionId = question.dataset.questionId;
        
        options.forEach(option => {
            option.addEventListener('change', function() {
                // Mark the question as answered in the navigation
                if (navButtons[index]) {
                    navButtons[index].classList.add('btn-success');
                    navButtons[index].classList.remove('btn-error', 'btn-warning');
                }
                
                // Update the answer count
                updateAnswerCount();
            });
        });
    });
    
    // Update the answer count display
    function updateAnswerCount() {
        const totalQuestions = questions.length;
        let answeredQuestions = 0;
        
        questions.forEach(question => {
            const options = question.querySelectorAll('input[type="radio"]:checked');
            if (options.length > 0) {
                answeredQuestions++;
            }
        });
        
        const answerCountElement = document.getElementById('quiz-answer-count');
        if (answerCountElement) {
            answerCountElement.textContent = `${answeredQuestions} of ${totalQuestions} questions answered`;
            
            // Update the color based on completion
            if (answeredQuestions === totalQuestions) {
                answerCountElement.classList.add('text-success');
                answerCountElement.classList.remove('text-warning', 'text-error');
            } else if (answeredQuestions >= totalQuestions / 2) {
                answerCountElement.classList.add('text-warning');
                answerCountElement.classList.remove('text-success', 'text-error');
            } else {
                answerCountElement.classList.add('text-error');
                answerCountElement.classList.remove('text-success', 'text-warning');
            }
        }
        
        // Enable/disable submit button
        const submitButton = document.getElementById('quiz-submit-button');
        if (submitButton) {
            submitButton.disabled = answeredQuestions < totalQuestions;
        }
    }
    
    // Initialize answer count
    updateAnswerCount();
}

/**
 * Initialize quiz submission
 */
function initQuizSubmission() {
    const quizForm = document.getElementById('quiz-form');
    if (!quizForm) return;
    
    quizForm.addEventListener('submit', function(event) {
        // Show confirmation dialog
        const confirmSubmit = document.getElementById('confirm-submit-modal');
        if (confirmSubmit) {
            event.preventDefault();
            confirmSubmit.classList.add('modal-open');
            
            // Handle confirm button
            const confirmButton = document.getElementById('confirm-submit-button');
            if (confirmButton) {
                confirmButton.addEventListener('click', function() {
                    quizForm.submit();
                });
            }
            
            // Handle cancel button
            const cancelButton = document.getElementById('cancel-submit-button');
            if (cancelButton) {
                cancelButton.addEventListener('click', function() {
                    confirmSubmit.classList.remove('modal-open');
                });
            }
        }
    });
}
