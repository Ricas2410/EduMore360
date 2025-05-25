"""
Install load testing tools for EduMore360
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"   ✅ {description} completed successfully")
            return True
        else:
            print(f"   ❌ {description} failed:")
            print(f"   Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ {description} failed with exception: {e}")
        return False

def install_requirements():
    """Install required packages for load testing"""
    print("📦 Installing Load Testing Requirements")
    print("=" * 50)
    
    # Required packages
    packages = [
        "locust",           # Load testing framework
        "psutil",           # System monitoring
        "requests",         # HTTP requests
        "memory-profiler",  # Memory monitoring
    ]
    
    success_count = 0
    
    for package in packages:
        if run_command(f"pip install {package}", f"Installing {package}"):
            success_count += 1
    
    print(f"\n📊 Installation Summary: {success_count}/{len(packages)} packages installed")
    
    if success_count == len(packages):
        print("🎉 All packages installed successfully!")
        return True
    else:
        print("❌ Some packages failed to install")
        return False

def verify_installation():
    """Verify that all tools are properly installed"""
    print("\n🔍 Verifying Installation")
    print("=" * 50)
    
    # Test imports
    test_imports = [
        ("locust", "Locust load testing framework"),
        ("psutil", "System monitoring"),
        ("requests", "HTTP requests"),
        ("memory_profiler", "Memory profiling"),
    ]
    
    success_count = 0
    
    for module, description in test_imports:
        try:
            __import__(module)
            print(f"   ✅ {description} - OK")
            success_count += 1
        except ImportError:
            print(f"   ❌ {description} - FAILED")
    
    print(f"\n📊 Verification Summary: {success_count}/{len(test_imports)} modules working")
    
    if success_count == len(test_imports):
        print("🎉 All tools verified successfully!")
        return True
    else:
        print("❌ Some tools are not working properly")
        return False

def create_test_directories():
    """Create necessary directories for testing"""
    print("\n📁 Creating Test Directories")
    print("=" * 50)
    
    directories = [
        "load_testing/results",
        "load_testing/logs",
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"   ✅ Created directory: {directory}")
        except Exception as e:
            print(f"   ❌ Failed to create {directory}: {e}")

def display_usage_instructions():
    """Display instructions for using the load testing tools"""
    print("\n" + "=" * 60)
    print("🎯 LOAD TESTING TOOLS READY!")
    print("=" * 60)
    
    print("\n📋 Quick Start Guide:")
    print("1. 🧪 Run quick system test:")
    print("   python load_testing/quick_test.py")
    
    print("\n2. 🔧 Setup test data:")
    print("   python load_testing/setup_load_test.py")
    
    print("\n3. 🚀 Start load testing:")
    print("   locust -f load_testing/locustfile.py --host=http://127.0.0.1:8000")
    print("   Then open: http://localhost:8089")
    
    print("\n4. 📊 Monitor performance (in another terminal):")
    print("   python load_testing/monitor_performance.py")
    
    print("\n🎯 Test Configuration for 2000 Users:")
    print("   - Number of users: 2000")
    print("   - Spawn rate: 50-100 users/second")
    print("   - Host: http://127.0.0.1:8000 (or your production URL)")
    
    print("\n📚 Documentation:")
    print("   - Read: LOAD_TESTING_GUIDE.md")
    print("   - Check results in: load_testing/results/")
    
    print("\n⚠️  Important Notes:")
    print("   - Test on production-like environment")
    print("   - Monitor CPU, memory, and database")
    print("   - Start with smaller user counts first")
    print("   - Have backup plans ready")

def main():
    """Main installation function"""
    print("🚀 EduMore360 Load Testing Tools Installer")
    print("=" * 60)
    print("This will install tools to test 2000 concurrent users")
    print("=" * 60)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("❌ Python 3.7+ required for load testing tools")
        print(f"   Current version: {python_version.major}.{python_version.minor}")
        return False
    
    print(f"✅ Python version: {python_version.major}.{python_version.minor} - OK")
    
    # Install requirements
    if not install_requirements():
        print("\n❌ Installation failed. Please check errors above.")
        return False
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Verification failed. Please check errors above.")
        return False
    
    # Create directories
    create_test_directories()
    
    # Display usage instructions
    display_usage_instructions()
    
    print("\n🎉 Load testing tools installation complete!")
    print("You're now ready to test your system with 2000 concurrent users!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
