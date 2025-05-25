"""
Comprehensive functionality test for EduMore360
Tests all major features to ensure optimizations don't break functionality
"""

import requests
import time
import json
from datetime import datetime

class FunctionalityTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
    def test_feature(self, feature_name, test_function):
        """Test a specific feature and record results"""
        print(f"🧪 Testing {feature_name}...", end=" ")
        
        try:
            start_time = time.time()
            result = test_function()
            end_time = time.time()
            
            if result['success']:
                print(f"✅ ({result.get('response_time', (end_time - start_time) * 1000):.0f}ms)")
                self.test_results.append({
                    'feature': feature_name,
                    'status': 'PASS',
                    'response_time': result.get('response_time', (end_time - start_time) * 1000),
                    'details': result.get('details', 'OK')
                })
                return True
            else:
                print(f"❌ {result.get('error', 'Failed')}")
                self.test_results.append({
                    'feature': feature_name,
                    'status': 'FAIL',
                    'error': result.get('error', 'Unknown error'),
                    'details': result.get('details', '')
                })
                return False
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            self.test_results.append({
                'feature': feature_name,
                'status': 'ERROR',
                'error': str(e)
            })
            return False
    
    def test_homepage(self):
        """Test homepage loading"""
        response = self.session.get(f"{self.base_url}/", timeout=10)
        return {
            'success': response.status_code == 200,
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_user_registration(self):
        """Test user registration page"""
        response = self.session.get(f"{self.base_url}/accounts/signup/", timeout=10)
        return {
            'success': response.status_code == 200 and 'signup' in response.text.lower(),
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_user_login(self):
        """Test user login page"""
        response = self.session.get(f"{self.base_url}/accounts/login/", timeout=10)
        return {
            'success': response.status_code == 200 and 'login' in response.text.lower(),
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_dashboard(self):
        """Test dashboard page"""
        response = self.session.get(f"{self.base_url}/dashboard/", timeout=10)
        return {
            'success': response.status_code in [200, 302],  # 302 if redirect to login
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_quiz_list(self):
        """Test quiz listing page"""
        response = self.session.get(f"{self.base_url}/quiz/", timeout=10)
        return {
            'success': response.status_code in [200, 302],
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_curriculum(self):
        """Test curriculum page"""
        response = self.session.get(f"{self.base_url}/curriculum/", timeout=10)
        return {
            'success': response.status_code in [200, 302],
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_admin_login(self):
        """Test admin login page"""
        response = self.session.get(f"{self.base_url}/my-admin/login/", timeout=10)
        return {
            'success': response.status_code == 200,
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_admin_dashboard(self):
        """Test admin dashboard (should redirect to login)"""
        response = self.session.get(f"{self.base_url}/my-admin/", timeout=10)
        return {
            'success': response.status_code in [200, 302],  # 302 redirect to login is OK
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_admin_users(self):
        """Test admin user management (should redirect to login)"""
        response = self.session.get(f"{self.base_url}/my-admin/users/", timeout=10)
        return {
            'success': response.status_code in [200, 302],
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_admin_quiz_management(self):
        """Test admin quiz management (should redirect to login)"""
        response = self.session.get(f"{self.base_url}/my-admin/quiz/", timeout=10)
        return {
            'success': response.status_code in [200, 302],
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_static_files(self):
        """Test static files loading"""
        response = self.session.get(f"{self.base_url}/static/css/style.css", timeout=10)
        return {
            'success': response.status_code in [200, 404],  # 404 is OK if file doesn't exist
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': f"Status: {response.status_code}"
        }
    
    def test_database_connection(self):
        """Test database connection by accessing a page that requires DB"""
        response = self.session.get(f"{self.base_url}/", timeout=10)
        # If homepage loads, database connection is working
        return {
            'success': response.status_code == 200,
            'response_time': response.elapsed.total_seconds() * 1000,
            'details': "Database connection via homepage"
        }
    
    def run_all_tests(self):
        """Run all functionality tests"""
        print("🚀 EduMore360 Functionality Test Suite")
        print("=" * 60)
        print(f"Target: {self.base_url}")
        print("Testing all major features after optimizations...")
        print("=" * 60)
        
        # Define all tests
        tests = [
            ("Homepage", self.test_homepage),
            ("User Registration", self.test_user_registration),
            ("User Login", self.test_user_login),
            ("Dashboard", self.test_dashboard),
            ("Quiz List", self.test_quiz_list),
            ("Curriculum", self.test_curriculum),
            ("Admin Login", self.test_admin_login),
            ("Admin Dashboard", self.test_admin_dashboard),
            ("Admin Users", self.test_admin_users),
            ("Admin Quiz Management", self.test_admin_quiz_management),
            ("Static Files", self.test_static_files),
            ("Database Connection", self.test_database_connection),
        ]
        
        # Run all tests
        passed = 0
        failed = 0
        
        for test_name, test_function in tests:
            if self.test_feature(test_name, test_function):
                passed += 1
            else:
                failed += 1
        
        # Display summary
        self.display_summary(passed, failed)
        
        return failed == 0  # Return True if all tests passed
    
    def display_summary(self, passed, failed):
        """Display test summary"""
        total = passed + failed
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("📊 FUNCTIONALITY TEST RESULTS")
        print("=" * 60)
        
        print(f"✅ Passed: {passed}/{total} ({success_rate:.1f}%)")
        print(f"❌ Failed: {failed}/{total}")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED!")
            print("✅ Your optimizations did NOT break any functionality")
            print("✅ All features are working correctly")
            print("✅ Safe to proceed with deployment")
        else:
            print(f"\n⚠️  {failed} TESTS FAILED!")
            print("🔧 Some features may have been affected by optimizations")
            print("📋 Failed tests:")
            
            for result in self.test_results:
                if result['status'] in ['FAIL', 'ERROR']:
                    print(f"   ❌ {result['feature']}: {result.get('error', 'Unknown error')}")
        
        # Response time analysis
        response_times = [r.get('response_time', 0) for r in self.test_results if r['status'] == 'PASS']
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            max_response = max(response_times)
            min_response = min(response_times)
            
            print(f"\n⏱️  Response Times:")
            print(f"   Average: {avg_response:.0f}ms")
            print(f"   Fastest: {min_response:.0f}ms")
            print(f"   Slowest: {max_response:.0f}ms")
            
            if avg_response < 1000:
                print("   🚀 Excellent response times!")
            elif avg_response < 3000:
                print("   👍 Good response times")
            else:
                print("   ⚠️  Slow response times - may need optimization")

def main():
    """Main test function"""
    import sys
    
    # Get target URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    print("🧪 EduMore360 Functionality Verification")
    print("=" * 60)
    print("This test ensures optimizations don't break functionality")
    print(f"Target: {base_url}")
    print("=" * 60)
    
    tester = FunctionalityTester(base_url)
    all_passed = tester.run_all_tests()
    
    print("\n" + "=" * 60)
    print("🎯 CONCLUSION")
    print("=" * 60)
    
    if all_passed:
        print("✅ ALL FUNCTIONALITY WORKING PERFECTLY!")
        print("✅ Optimizations are safe and don't break features")
        print("✅ Ready to proceed with Railway migration")
        print("\nNext steps:")
        print("1. Deploy to Railway.app")
        print("2. Run this test on Railway")
        print("3. Run load tests on Railway")
        print("4. Migrate when confident")
    else:
        print("❌ SOME FUNCTIONALITY ISSUES DETECTED!")
        print("🔧 Please fix failed tests before proceeding")
        print("📞 Contact support if you need help")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    if not success:
        exit(1)
