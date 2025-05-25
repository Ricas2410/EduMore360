# 🚀 EduMore360 PythonAnywhere Deployment Guide

## 📋 **Complete Setup Process**

This directory contains all the scripts and configurations needed to deploy EduMore360 on PythonAnywhere.

### 🗂️ **Files Overview:**

1. **`setup_pythonanywhere.sh`** - Main setup script
2. **`pythonanywhere_settings.py`** - Django settings for PythonAnywhere
3. **`pythonanywhere_wsgi.py`** - WSGI configuration
4. **`pythonanywhere.env`** - Environment variables template
5. **`requirements_pythonanywhere.txt`** - Python dependencies
6. **`migrate_and_setup.py`** - Database setup script
7. **`static_setup.sh`** - Static files configuration
8. **`update_gitignore.txt`** - Updated .gitignore content

### 🎯 **Deployment Steps:**

#### **Step 1: Clean Setup**
```bash
# On PythonAnywhere console
cd /home/edumore360
rm -rf EduMore360  # Remove existing directory
```

#### **Step 2: Clone Repository**
```bash
git clone https://github.com/Ricas2410/EduMore360.git
cd EduMore360
```

#### **Step 3: Run Setup Script**
```bash
chmod +x pythonanywhere_setup/setup_pythonanywhere.sh
./pythonanywhere_setup/setup_pythonanywhere.sh
```

#### **Step 4: Configure Web App**
- Go to PythonAnywhere Web tab
- Create new web app (Python 3.10, Manual configuration)
- Update WSGI file with provided configuration
- Set static files mappings

#### **Step 5: Final Setup**
```bash
python pythonanywhere_setup/migrate_and_setup.py
```

### 🌟 **Features Included:**

- ✅ SQLite database configuration
- ✅ Wasabi S3 storage for media files
- ✅ Static files optimization
- ✅ Environment variables setup
- ✅ Security configurations
- ✅ Performance optimizations
- ✅ Error handling
- ✅ Admin user creation
- ✅ Sample data loading

### 🔧 **Manual Configuration Required:**

1. **Environment Variables**: Update `pythonanywhere.env` with your values
2. **Domain Settings**: Update ALLOWED_HOSTS in settings
3. **Static Files**: Configure in PythonAnywhere web tab
4. **SSL Certificate**: Enable HTTPS (optional)

### 📞 **Support:**

If you encounter any issues:
1. Check the error logs in PythonAnywhere
2. Verify environment variables are set correctly
3. Ensure all dependencies are installed
4. Check static files configuration

---

**Ready to deploy your world-class educational platform!** 🎓✨
