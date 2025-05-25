# 🚀 EduMore360 PythonAnywhere Professional Deployment

## 📋 **One-Command Professional Deployment**

This guide provides the **fastest and most reliable** way to deploy EduMore360 on PythonAnywhere using your existing configuration.

---

## 🚀 **Complete Deployment Process**

### **Step 1: Access PythonAnywhere Console**
1. Login to your PythonAnywhere account
2. Go to **"Consoles"** tab
3. Start a **"Bash"** console

### **Step 2: Clean Deployment**
```bash
# Remove any existing installation
cd /home/edumore360
rm -rf EduMore360

# Clone fresh repository
git clone https://github.com/Ricas2410/EduMore360.git
cd EduMore360

# Run professional deployment script
chmod +x pythonanywhere_setup/quick_deploy.sh
./pythonanywhere_setup/quick_deploy.sh
```

### **Step 3: Update Domain in Environment**
```bash
# Edit the environment file
nano .env

# Change this line:
# ALLOWED_HOSTS=localhost,127.0.0.1,yourusername.pythonanywhere.com
# To (replace 'edumore360' with your actual username):
ALLOWED_HOSTS=localhost,127.0.0.1,edumore360.pythonanywhere.com
```

### **Step 4: Create PythonAnywhere Web App**
1. Go to **"Web"** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

### **Step 5: Configure Web App Settings**

#### **Source Code & Working Directory:**
- **Source code**: `/home/edumore360/EduMore360`
- **Working directory**: `/home/edumore360/EduMore360`

#### **WSGI Configuration:**
1. Click on **WSGI configuration file** link
2. **Replace ALL content** with:
```python
import os
import sys

path = '/home/edumore360/EduMore360'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edumore360.settings_pythonanywhere')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### **Static Files Configuration:**
In the **"Static files"** section, add:
- **URL**: `/static/`
- **Directory**: `/home/edumore360/EduMore360/staticfiles/`

#### **Media Files Configuration:**
In the **"Static files"** section, add:
- **URL**: `/media/`
- **Directory**: `/home/edumore360/EduMore360/media/`

### **Step 6: Launch Your Site**
1. Click **"Reload"** button in Web tab
2. Visit: `https://edumore360.pythonanywhere.com`
3. Login to admin: `https://edumore360.pythonanywhere.com/my-admin/`

**Default Admin Credentials:**
- **Email**: `admin@edumore360.com`
- **Password**: `admin123`

---

## ✅ **Verification & Testing**

### **Step 1: Test Your Deployment**
1. **Homepage**: Visit `https://edumore360.pythonanywhere.com`
2. **Admin Panel**: Visit `https://edumore360.pythonanywhere.com/my-admin/`
3. **User Registration**: Test student signup
4. **Quiz System**: Create and take a quiz

### **Step 2: Change Admin Password**
1. Login to admin with default credentials
2. Go to User Management
3. Edit admin user and change password

### **Step 3: Verify Media Upload**
1. Try uploading a profile picture
2. Check if it appears in your Wasabi bucket
3. Verify images load correctly on the site

---

## � **Troubleshooting**

### **Common Issues:**

#### **1. Site Not Loading**
- Check error logs in PythonAnywhere Web tab
- Verify WSGI configuration is correct
- Ensure virtual environment is activated

#### **2. Static Files Missing**
- Verify static files path: `/home/edumore360/EduMore360/staticfiles/`
- Run: `python manage.py collectstatic --noinput`

#### **3. Database Errors**
- Run: `python manage.py migrate`
- Check if SQLite file exists and has permissions

#### **4. Media Upload Issues**
- Verify Wasabi credentials in `.env`
- Check bucket permissions (should be public)

---

## 🔄 **Updating Your Site**

When you make changes to your code:

```bash
cd /home/edumore360/EduMore360
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Then click **"Reload"** in PythonAnywhere Web tab.

---

## 🧪 **Testing Your Deployment**

### **Step 1: Check Admin Access**
Visit: `https://yourusername.pythonanywhere.com/my-admin/`

**Default credentials:**
- Email: `admin@edumore360.com`
- Password: `admin123`

### **Step 2: Test File Upload**
1. Login to admin
2. Try uploading a profile picture
3. Verify it appears in Wasabi bucket

### **Step 3: Test Quiz System**
1. Go to Quiz Management
2. Create a test quiz
3. Take the quiz as a student

---

## 🔧 **Troubleshooting**

### **Common Issues:**

#### **1. ImportError or Module Not Found**
```bash
cd /home/edumore360/EduMore360
source venv/bin/activate
pip install -r pythonanywhere_setup/requirements_pythonanywhere.txt
```

#### **2. Static Files Not Loading**
Check static files configuration in Web tab:
- URL: `/static/`
- Directory: `/home/edumore360/EduMore360/staticfiles/`

#### **3. Database Errors**
```bash
cd /home/edumore360/EduMore360
source venv/bin/activate
python manage.py migrate
```

#### **4. Media Files Not Uploading**
Verify Wasabi credentials in `.env` file

#### **5. 500 Internal Server Error**
Check error logs in PythonAnywhere Web tab

---

## 📈 **Performance Optimization**

### **Enable Caching**
Already configured in settings for better performance.

### **Optimize Images**
Use compressed images for better loading times.

### **Monitor Usage**
Check PythonAnywhere dashboard for resource usage.

---

## 🔄 **Updating Your Site**

### **Pull Latest Changes**
```bash
cd /home/edumore360/EduMore360
git pull origin main
source venv/bin/activate
pip install -r pythonanywhere_setup/requirements_pythonanywhere.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

### **Reload Web App**
Click "Reload" in PythonAnywhere Web tab.

---

## 🎉 **Success Checklist**

- ✅ Web app loads without errors
- ✅ Admin panel accessible
- ✅ Static files loading correctly
- ✅ Media files uploading to Wasabi
- ✅ Quiz system working
- ✅ User registration working
- ✅ Mobile responsive design
- ✅ SSL certificate enabled (optional)

---

## 📞 **Support**

If you encounter issues:
1. Check PythonAnywhere error logs
2. Verify all environment variables
3. Ensure Wasabi credentials are correct
4. Check static files configuration

**Your EduMore360 platform is now live on PythonAnywhere!** 🚀🎓
