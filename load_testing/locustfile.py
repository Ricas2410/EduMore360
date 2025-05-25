"""
Load Testing Script for EduMore360
Tests 2000 concurrent users taking quizzes and learning
"""

from locust import HttpUser, task, between
import random
import json

class EduMore360User(HttpUser):
    wait_time = between(1, 5)  # Wait 1-5 seconds between requests
    
    def on_start(self):
        """Called when a user starts - simulates user registration/login"""
        # Register a new user
        self.register_user()
        # Login
        self.login_user()
        # Get CSRF token
        self.get_csrf_token()
    
    def register_user(self):
        """Register a new user"""
        user_id = random.randint(10000, 99999)
        self.email = f"testuser{user_id}@example.com"
        self.password = "testpass123"
        
        response = self.client.post("/accounts/signup/", {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        }, catch_response=True)
        
        if response.status_code in [200, 302]:
            response.success()
        else:
            response.failure(f"Registration failed: {response.status_code}")
    
    def login_user(self):
        """Login the user"""
        response = self.client.post("/accounts/login/", {
            "login": self.email,
            "password": self.password,
        }, catch_response=True)
        
        if response.status_code in [200, 302]:
            response.success()
        else:
            response.failure(f"Login failed: {response.status_code}")
    
    def get_csrf_token(self):
        """Get CSRF token for forms"""
        response = self.client.get("/")
        if 'csrftoken' in self.client.cookies:
            self.csrf_token = self.client.cookies['csrftoken']
        else:
            self.csrf_token = None
    
    @task(3)
    def browse_dashboard(self):
        """Browse the main dashboard - most common action"""
        with self.client.get("/dashboard/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Dashboard failed: {response.status_code}")
    
    @task(2)
    def browse_quizzes(self):
        """Browse available quizzes"""
        with self.client.get("/quiz/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Quiz browse failed: {response.status_code}")
    
    @task(2)
    def view_curriculum(self):
        """View curriculum content"""
        with self.client.get("/curriculum/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Curriculum failed: {response.status_code}")
    
    @task(1)
    def take_quiz(self):
        """Simulate taking a quiz - most resource intensive"""
        # First get available quizzes
        response = self.client.get("/quiz/")
        if response.status_code != 200:
            return
        
        # Simulate starting a quiz (you'll need to adjust the URL)
        quiz_id = random.randint(1, 10)  # Assuming you have quizzes with IDs 1-10
        
        with self.client.get(f"/quiz/{quiz_id}/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Quiz start failed: {response.status_code}")
        
        # Simulate answering questions
        for question_num in range(1, 6):  # Simulate 5 questions
            answer_data = {
                'question_id': question_num,
                'answer': random.choice(['A', 'B', 'C', 'D']),
                'csrfmiddlewaretoken': self.csrf_token
            }
            
            with self.client.post(f"/quiz/{quiz_id}/answer/", 
                                data=answer_data, 
                                catch_response=True) as response:
                if response.status_code in [200, 302]:
                    response.success()
                else:
                    response.failure(f"Quiz answer failed: {response.status_code}")
    
    @task(1)
    def view_notes(self):
        """View study notes"""
        with self.client.get("/notes/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Notes failed: {response.status_code}")
    
    @task(1)
    def view_profile(self):
        """View user profile"""
        with self.client.get("/profile/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Profile failed: {response.status_code}")

class AdminUser(HttpUser):
    """Simulate admin users accessing admin panel"""
    wait_time = between(5, 15)  # Admins take longer between actions
    weight = 1  # Much fewer admin users
    
    def on_start(self):
        """Login as admin"""
        self.client.post("/my-admin/login/", {
            "username": "admin@edumore360.com",
            "password": "your-admin-password"
        })
    
    @task(2)
    def admin_dashboard(self):
        """View admin dashboard"""
        with self.client.get("/my-admin/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Admin dashboard failed: {response.status_code}")
    
    @task(1)
    def admin_users(self):
        """View user management"""
        with self.client.get("/my-admin/users/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Admin users failed: {response.status_code}")
    
    @task(1)
    def admin_quizzes(self):
        """View quiz management"""
        with self.client.get("/my-admin/quiz/", catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Admin quizzes failed: {response.status_code}")

# Test scenarios
class QuizTakingUser(HttpUser):
    """Users focused on taking quizzes"""
    wait_time = between(2, 8)
    weight = 3  # More quiz-focused users
    
    def on_start(self):
        user_id = random.randint(100000, 999999)
        self.email = f"quizuser{user_id}@example.com"
        self.password = "testpass123"
        
        # Quick registration and login
        self.client.post("/accounts/signup/", {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        })
        
        self.client.post("/accounts/login/", {
            "login": self.email,
            "password": self.password,
        })
    
    @task(5)
    def take_multiple_quizzes(self):
        """Take multiple quizzes in sequence"""
        for quiz_id in range(1, 4):  # Take 3 quizzes
            self.client.get(f"/quiz/{quiz_id}/")
            
            # Answer questions quickly
            for q in range(1, 6):
                self.client.post(f"/quiz/{quiz_id}/answer/", {
                    'question_id': q,
                    'answer': random.choice(['A', 'B', 'C', 'D'])
                })

class LearningUser(HttpUser):
    """Users focused on learning content"""
    wait_time = between(3, 10)
    weight = 2  # Moderate number of learning users
    
    def on_start(self):
        user_id = random.randint(100000, 999999)
        self.email = f"learner{user_id}@example.com"
        self.password = "testpass123"
        
        self.client.post("/accounts/signup/", {
            "email": self.email,
            "password1": self.password,
            "password2": self.password,
        })
        
        self.client.post("/accounts/login/", {
            "login": self.email,
            "password": self.password,
        })
    
    @task(3)
    def study_content(self):
        """Study notes and curriculum"""
        self.client.get("/curriculum/")
        self.client.get("/notes/")
        
        # Simulate reading time
        import time
        time.sleep(random.uniform(2, 5))
    
    @task(1)
    def occasional_quiz(self):
        """Take occasional quiz"""
        quiz_id = random.randint(1, 5)
        self.client.get(f"/quiz/{quiz_id}/")
