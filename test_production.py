"""
Test EduMore360 production site for 2000 concurrent users
Run this from your local machine to test https://edumore360.onrender.com/
"""

import requests
import time
import threading
import random
from datetime import datetime
import json

class ProductionTester:
    def __init__(self, base_url="https://edumore360.onrender.com"):
        self.base_url = base_url
        self.results = []
        self.active_users = 0
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.response_times = []
        self.errors = []
        self.running = False
        
    def simulate_user(self, user_id, duration=300):
        """Simulate a single user for specified duration (seconds)"""
        session = requests.Session()
        user_results = []
        
        try:
            self.active_users += 1
            start_time = time.time()
            
            while time.time() - start_time < duration and self.running:
                # Random user behavior
                action = random.choice([
                    'homepage', 'homepage', 'homepage',  # Most common
                    'dashboard', 'dashboard',
                    'quiz_list', 'quiz_list',
                    'curriculum',
                    'register',
                    'login'
                ])
                
                result = self.perform_action(session, action, user_id)
                user_results.append(result)
                
                # Update global stats
                self.total_requests += 1
                if result['success']:
                    self.successful_requests += 1
                    self.response_times.append(result['response_time'])
                else:
                    self.failed_requests += 1
                    self.errors.append(result.get('error', 'Unknown error'))
                
                # Wait between requests (1-5 seconds)
                time.sleep(random.uniform(1, 5))
                
        except Exception as e:
            self.errors.append(f"User {user_id} crashed: {str(e)}")
        finally:
            self.active_users -= 1
            
        return user_results
    
    def perform_action(self, session, action, user_id):
        """Perform a specific user action"""
        start_time = time.time()
        
        try:
            if action == 'homepage':
                response = session.get(f"{self.base_url}/", timeout=30)
            elif action == 'dashboard':
                response = session.get(f"{self.base_url}/dashboard/", timeout=30)
            elif action == 'quiz_list':
                response = session.get(f"{self.base_url}/quiz/", timeout=30)
            elif action == 'curriculum':
                response = session.get(f"{self.base_url}/curriculum/", timeout=30)
            elif action == 'register':
                response = session.get(f"{self.base_url}/accounts/signup/", timeout=30)
            elif action == 'login':
                response = session.get(f"{self.base_url}/accounts/login/", timeout=30)
            else:
                response = session.get(f"{self.base_url}/", timeout=30)
            
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            return {
                'user_id': user_id,
                'action': action,
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': round(response_time, 2),
                'timestamp': datetime.now().isoformat(),
                'content_length': len(response.content) if response.status_code == 200 else 0
            }
            
        except requests.exceptions.Timeout:
            return {
                'user_id': user_id,
                'action': action,
                'success': False,
                'error': 'Timeout (>30s)',
                'response_time': 30000,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'user_id': user_id,
                'action': action,
                'success': False,
                'error': str(e),
                'response_time': 0,
                'timestamp': datetime.now().isoformat()
            }
    
    def monitor_progress(self):
        """Monitor and display progress"""
        while self.running:
            success_rate = (self.successful_requests / max(self.total_requests, 1)) * 100
            avg_response_time = sum(self.response_times) / max(len(self.response_times), 1)
            
            print(f"\r🔍 Active Users: {self.active_users:4d} | "
                  f"Requests: {self.total_requests:5d} | "
                  f"Success: {success_rate:5.1f}% | "
                  f"Avg Response: {avg_response_time:6.1f}ms", end="")
            
            time.sleep(2)
    
    def run_load_test(self, max_users=100, ramp_up_time=60, test_duration=300):
        """Run load test with gradual user ramp-up"""
        print(f"🚀 Starting Load Test on {self.base_url}")
        print(f"📊 Target: {max_users} users over {ramp_up_time}s ramp-up, {test_duration}s duration")
        print("=" * 80)
        
        self.running = True
        threads = []
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_progress)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        # Gradually add users
        users_per_second = max_users / ramp_up_time
        
        for i in range(max_users):
            if not self.running:
                break
                
            # Create user thread
            user_thread = threading.Thread(
                target=self.simulate_user, 
                args=(i + 1, test_duration)
            )
            user_thread.daemon = True
            user_thread.start()
            threads.append(user_thread)
            
            # Wait before adding next user
            if i < max_users - 1:
                time.sleep(1 / users_per_second)
        
        print(f"\n✅ All {max_users} users started!")
        print("⏳ Running test... Press Ctrl+C to stop early")
        
        try:
            # Wait for test to complete
            time.sleep(test_duration)
        except KeyboardInterrupt:
            print("\n🛑 Test stopped by user")
        
        # Stop the test
        self.running = False
        
        # Wait for threads to finish (with timeout)
        print("\n⏳ Waiting for users to finish...")
        for thread in threads:
            thread.join(timeout=10)
        
        self.display_results()
    
    def display_results(self):
        """Display test results"""
        print("\n" + "=" * 80)
        print("📊 LOAD TEST RESULTS")
        print("=" * 80)
        
        if self.total_requests == 0:
            print("❌ No requests completed")
            return
        
        # Calculate statistics
        success_rate = (self.successful_requests / self.total_requests) * 100
        error_rate = (self.failed_requests / self.total_requests) * 100
        
        if self.response_times:
            avg_response_time = sum(self.response_times) / len(self.response_times)
            min_response_time = min(self.response_times)
            max_response_time = max(self.response_times)
            
            # Calculate percentiles
            sorted_times = sorted(self.response_times)
            p95_index = int(0.95 * len(sorted_times))
            p95_response_time = sorted_times[p95_index] if p95_index < len(sorted_times) else max_response_time
        else:
            avg_response_time = 0
            min_response_time = 0
            max_response_time = 0
            p95_response_time = 0
        
        # Display results
        print(f"📈 Total Requests: {self.total_requests}")
        print(f"✅ Successful: {self.successful_requests} ({success_rate:.1f}%)")
        print(f"❌ Failed: {self.failed_requests} ({error_rate:.1f}%)")
        print()
        print(f"⏱️  Response Times:")
        print(f"   Average: {avg_response_time:.1f}ms")
        print(f"   Minimum: {min_response_time:.1f}ms")
        print(f"   Maximum: {max_response_time:.1f}ms")
        print(f"   95th Percentile: {p95_response_time:.1f}ms")
        
        # Performance assessment
        print("\n🎯 PERFORMANCE ASSESSMENT:")
        
        if success_rate >= 95 and avg_response_time < 3000:
            print("🎉 EXCELLENT! Your site can handle this load very well!")
        elif success_rate >= 90 and avg_response_time < 5000:
            print("👍 GOOD! Your site handles this load acceptably.")
        elif success_rate >= 80 and avg_response_time < 10000:
            print("⚠️  FAIR! Your site struggles but works under this load.")
        else:
            print("❌ POOR! Your site cannot handle this load reliably.")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        
        if error_rate > 10:
            print("   🔧 High error rate - check server logs and optimize")
        
        if avg_response_time > 5000:
            print("   ⚡ Slow response times - optimize database and caching")
        
        if success_rate < 95:
            print("   🛠️  Reliability issues - investigate failed requests")
        
        # Common errors
        if self.errors:
            error_counts = {}
            for error in self.errors:
                error_counts[error] = error_counts.get(error, 0) + 1
            
            print("\n🚨 COMMON ERRORS:")
            for error, count in sorted(error_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"   {count}x: {error}")

def main():
    """Main function"""
    print("🧪 EduMore360 Production Load Tester")
    print("Testing: https://edumore360.onrender.com/")
    print("=" * 80)
    
    tester = ProductionTester()
    
    # Test scenarios
    scenarios = [
        (50, 30, 120),    # 50 users, 30s ramp-up, 2min test
        (100, 60, 180),   # 100 users, 1min ramp-up, 3min test
        (200, 120, 300),  # 200 users, 2min ramp-up, 5min test
        (500, 300, 600),  # 500 users, 5min ramp-up, 10min test
    ]
    
    print("📋 Available test scenarios:")
    for i, (users, ramp, duration) in enumerate(scenarios, 1):
        print(f"   {i}. {users} users ({ramp}s ramp-up, {duration//60}min duration)")
    
    print("   5. Custom test")
    print("   6. Quick test (10 users, 30 seconds)")
    
    try:
        choice = input("\nSelect scenario (1-6): ").strip()
        
        if choice == "6":
            # Quick test
            tester.run_load_test(max_users=10, ramp_up_time=10, test_duration=30)
        elif choice in ["1", "2", "3", "4"]:
            users, ramp, duration = scenarios[int(choice) - 1]
            print(f"\n⚠️  WARNING: Testing {users} users on production!")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                tester.run_load_test(max_users=users, ramp_up_time=ramp, test_duration=duration)
            else:
                print("Test cancelled.")
        elif choice == "5":
            # Custom test
            users = int(input("Number of users: "))
            ramp = int(input("Ramp-up time (seconds): "))
            duration = int(input("Test duration (seconds): "))
            
            print(f"\n⚠️  WARNING: Testing {users} users on production!")
            confirm = input("Are you sure? (yes/no): ").lower()
            if confirm == 'yes':
                tester.run_load_test(max_users=users, ramp_up_time=ramp, test_duration=duration)
            else:
                print("Test cancelled.")
        else:
            print("Invalid choice. Running quick test...")
            tester.run_load_test(max_users=10, ramp_up_time=10, test_duration=30)
            
    except KeyboardInterrupt:
        print("\n🛑 Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
