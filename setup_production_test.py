"""
Setup script for testing EduMore360 production site
Installs required tools and runs tests against https://edumore360.onrender.com/
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages for production testing"""
    print("📦 Installing Production Testing Requirements")
    print("=" * 50)
    
    packages = ["requests", "threading"]  # Basic packages for testing
    
    for package in packages:
        try:
            print(f"🔧 Installing {package}...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError:
            print(f"   ⚠️  {package} may already be installed")
        except Exception as e:
            print(f"   ❌ Failed to install {package}: {e}")

def test_connection():
    """Test connection to production site"""
    print("\n🔍 Testing Connection to Production Site")
    print("=" * 50)
    
    try:
        import requests
        
        print("🌐 Testing https://edumore360.onrender.com/...")
        response = requests.get("https://edumore360.onrender.com/", timeout=30)
        
        if response.status_code == 200:
            print(f"   ✅ Site is accessible! Response time: {response.elapsed.total_seconds():.2f}s")
            return True
        else:
            print(f"   ⚠️  Site returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ Site is too slow (>30s timeout)")
        return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Cannot connect to site")
        return False
    except Exception as e:
        print(f"   ❌ Error testing site: {e}")
        return False

def display_instructions():
    """Display testing instructions"""
    print("\n" + "=" * 60)
    print("🎯 PRODUCTION TESTING READY!")
    print("=" * 60)
    
    print("\n📋 How to Test Your Production Site:")
    print("1. 🧪 Run the production test:")
    print("   python test_production.py")
    
    print("\n2. 📊 Choose a test scenario:")
    print("   - Quick test: 10 users for 30 seconds")
    print("   - Small test: 50 users for 2 minutes")
    print("   - Medium test: 100 users for 3 minutes")
    print("   - Large test: 200 users for 5 minutes")
    print("   - Stress test: 500 users for 10 minutes")
    
    print("\n🎯 Recommended Testing Strategy:")
    print("1. Start with Quick test (10 users)")
    print("2. If successful, try Small test (50 users)")
    print("3. Gradually increase to 100, 200, 500 users")
    print("4. Monitor Render dashboard for memory usage")
    print("5. Stop if you see memory errors or crashes")
    
    print("\n⚠️  IMPORTANT WARNINGS:")
    print("- You're testing on PRODUCTION with 512MB memory")
    print("- High load may cause temporary slowdowns")
    print("- Monitor your Render dashboard during tests")
    print("- Stop immediately if you see errors")
    print("- Don't run tests when real users are active")
    
    print("\n📊 Success Criteria for 2000 Users:")
    print("✅ 500 users test passes with <5% errors")
    print("✅ Average response time <5 seconds")
    print("✅ No memory crashes on Render")
    print("✅ Site remains accessible during test")
    
    print("\n🚨 If Tests Fail:")
    print("- Check Render logs for memory errors")
    print("- Consider upgrading Render plan")
    print("- Optimize database queries further")
    print("- Add caching (Redis)")
    print("- Consider Railway.app ($5/month alternative)")

def main():
    """Main setup function"""
    print("🚀 EduMore360 Production Testing Setup")
    print("=" * 60)
    print("Target: https://edumore360.onrender.com/")
    print("Memory Limit: 512MB (Render)")
    print("=" * 60)
    
    # Install requirements
    install_requirements()
    
    # Test connection
    if not test_connection():
        print("\n❌ Cannot connect to production site!")
        print("Please check:")
        print("- Is your site deployed and running?")
        print("- Is the URL correct?")
        print("- Are there any deployment errors?")
        return False
    
    # Display instructions
    display_instructions()
    
    print("\n🎉 Setup complete! Ready to test production site.")
    print("\nNext step: python test_production.py")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
