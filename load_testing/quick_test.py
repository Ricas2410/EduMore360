"""
Quick system readiness test for EduMore360
Tests basic functionality before running full load tests
"""

import requests
import time
import json
from datetime import datetime

class QuickSystemTest:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.results = []
        self.session = requests.Session()
    
    def test_endpoint(self, endpoint, expected_status=200, timeout=10):
        """Test a single endpoint"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=timeout)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            
            result = {
                'endpoint': endpoint,
                'url': url,
                'status_code': response.status_code,
                'response_time_ms': round(response_time, 2),
                'expected_status': expected_status,
                'success': response.status_code == expected_status,
                'content_length': len(response.content),
                'timestamp': datetime.now().isoformat()
            }
            
            # Check for common error indicators
            if response.status_code == 200:
                content = response.text.lower()
                if 'error' in content or 'exception' in content or 'traceback' in content:
                    result['success'] = False
                    result['warning'] = 'Error content detected in response'
            
            return result
            
        except requests.exceptions.Timeout:
            return {
                'endpoint': endpoint,
                'url': url,
                'success': False,
                'error': 'Timeout',
                'response_time_ms': timeout * 1000,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'endpoint': endpoint,
                'url': url,
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def test_user_registration(self):
        """Test user registration functionality"""
        print("🧪 Testing user registration...")
        
        # Test registration page
        reg_page = self.test_endpoint("/accounts/signup/")
        if not reg_page['success']:
            return reg_page
        
        # Try to register a test user
        test_email = f"test_{int(time.time())}@example.com"
        
        try:
            # Get CSRF token first
            response = self.session.get(f"{self.base_url}/accounts/signup/")
            
            # Extract CSRF token (simplified)
            csrf_token = None
            if 'csrftoken' in self.session.cookies:
                csrf_token = self.session.cookies['csrftoken']
            
            # Attempt registration
            reg_data = {
                'email': test_email,
                'password1': 'testpass123',
                'password2': 'testpass123',
            }
            
            if csrf_token:
                reg_data['csrfmiddlewaretoken'] = csrf_token
            
            start_time = time.time()
            response = self.session.post(f"{self.base_url}/accounts/signup/", data=reg_data)
            end_time = time.time()
            
            return {
                'endpoint': '/accounts/signup/ (POST)',
                'success': response.status_code in [200, 302],
                'status_code': response.status_code,
                'response_time_ms': round((end_time - start_time) * 1000, 2),
                'test_email': test_email,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'endpoint': '/accounts/signup/ (POST)',
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def run_basic_tests(self):
        """Run basic functionality tests"""
        print("🚀 Running EduMore360 System Readiness Test")
        print("=" * 60)
        
        # Define test endpoints
        test_endpoints = [
            ('/', 'Homepage'),
            ('/accounts/signup/', 'User Registration'),
            ('/accounts/login/', 'User Login'),
            ('/dashboard/', 'Dashboard'),
            ('/quiz/', 'Quiz List'),
            ('/curriculum/', 'Curriculum'),
            ('/my-admin/login/', 'Admin Login'),
            ('/my-admin/', 'Admin Dashboard'),
            ('/my-admin/users/', 'User Management'),
            ('/my-admin/quiz/', 'Quiz Management'),
        ]
        
        print("🔍 Testing core endpoints...")
        
        all_passed = True
        total_response_time = 0
        successful_tests = 0
        
        for endpoint, description in test_endpoints:
            print(f"   Testing {description}...", end=" ")
            
            result = self.test_endpoint(endpoint)
            self.results.append(result)
            
            if result['success']:
                print(f"✅ {result['response_time_ms']}ms")
                total_response_time += result['response_time_ms']
                successful_tests += 1
            else:
                print(f"❌ {result.get('error', 'Failed')}")
                all_passed = False
        
        # Test user registration
        print("\n🧪 Testing user registration...")
        reg_result = self.test_user_registration()
        self.results.append(reg_result)
        
        if reg_result['success']:
            print("   ✅ User registration working")
        else:
            print(f"   ❌ User registration failed: {reg_result.get('error', 'Unknown error')}")
            all_passed = False
        
        # Calculate average response time
        avg_response_time = total_response_time / successful_tests if successful_tests > 0 else 0
        
        # Display summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        print(f"✅ Successful tests: {successful_tests}/{len(test_endpoints)}")
        print(f"⏱️  Average response time: {avg_response_time:.2f}ms")
        
        if all_passed:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Your system is ready for load testing")
            
            if avg_response_time < 1000:
                print("🚀 Excellent response times - system looks very fast!")
            elif avg_response_time < 3000:
                print("👍 Good response times - should handle load well")
            else:
                print("⚠️  Slow response times - consider optimization before load testing")
                
        else:
            print("\n❌ SOME TESTS FAILED!")
            print("🔧 Please fix the failing endpoints before running load tests")
        
        return all_passed, avg_response_time
    
    def save_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"load_testing/quick_test_results_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\n📄 Detailed results saved to: {filename}")
        except Exception as e:
            print(f"❌ Error saving results: {e}")

def main():
    """Main function"""
    import sys
    
    # Get target URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    print("🧪 EduMore360 Quick System Test")
    print("=" * 60)
    print(f"Target URL: {base_url}")
    print("Testing basic functionality before load testing...")
    print("=" * 60)
    
    tester = QuickSystemTest(base_url)
    all_passed, avg_response_time = tester.run_basic_tests()
    tester.save_results()
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS")
    print("=" * 60)
    
    if all_passed:
        print("1. ✅ Basic tests passed - system is functional")
        print("2. 🚀 Run load testing setup: python load_testing/setup_load_test.py")
        print("3. 🧪 Install locust: pip install locust")
        print("4. 📊 Run load test: locust -f load_testing/locustfile.py --host=" + base_url)
        print("5. 🔍 Monitor performance: python load_testing/monitor_performance.py " + base_url)
        
        if avg_response_time > 3000:
            print("\n⚠️  WARNING: Slow response times detected")
            print("   Consider optimizing before testing with 2000 users")
            
    else:
        print("1. ❌ Fix the failing endpoints first")
        print("2. 🔧 Check server logs for errors")
        print("3. 🔄 Run this test again: python load_testing/quick_test.py")
        print("4. 📞 Get help if needed")

if __name__ == "__main__":
    main()
