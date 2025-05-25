# 🚀 EduMore360 PythonAnywhere Deployment Instructions

## 📋 **Complete Step-by-Step Guide**

### 🎯 **Prerequisites**
- PythonAnywhere account (free tier is fine)
- Wasabi S3 account for media storage
- GitHub repository access

---

## 🚀 **Method 1: Quick Deployment (Recommended)**

### **Step 1: Access PythonAnywhere Console**
1. Login to your PythonAnywhere account
2. Go to **"Consoles"** tab
3. Start a **"Bash"** console

### **Step 2: Run Quick Deployment**
```bash
cd /home/edumore360
wget https://raw.githubusercontent.com/Ricas2410/EduMore360/main/pythonanywhere_setup/quick_deploy.sh
chmod +x quick_deploy.sh
./quick_deploy.sh
```

### **Step 3: Configure Environment Variables**
```bash
cd EduMore360
nano .env
```

Update these values:
```env
SECRET_KEY=your-new-secret-key-here
WASABI_ACCESS_KEY_ID=your-wasabi-access-key
WASABI_SECRET_ACCESS_KEY=your-wasabi-secret-key
WASABI_STORAGE_BUCKET_NAME=your-bucket-name
```

### **Step 4: Configure Web App**
1. Go to **"Web"** tab in PythonAnywhere
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

### **Step 5: Set Paths**
- **Source code**: `/home/edumore360/EduMore360`
- **Working directory**: `/home/edumore360/EduMore360`

### **Step 6: Configure WSGI**
1. Click on **WSGI configuration file** link
2. Replace content with:
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

### **Step 7: Configure Static Files**
In the **"Static files"** section, add:
- **URL**: `/static/`
- **Directory**: `/home/edumore360/EduMore360/staticfiles/`

### **Step 8: Configure Media Files**
In the **"Static files"** section, add:
- **URL**: `/media/`
- **Directory**: `/home/edumore360/EduMore360/media/`

### **Step 9: Reload Web App**
Click **"Reload"** button

---

## 🔧 **Method 2: Manual Deployment**

### **Step 1: Clean Setup**
```bash
cd /home/edumore360
rm -rf EduMore360
```

### **Step 2: Clone Repository**
```bash
git clone https://github.com/Ricas2410/EduMore360.git
cd EduMore360
```

### **Step 3: Run Setup Script**
```bash
chmod +x pythonanywhere_setup/setup_pythonanywhere.sh
./pythonanywhere_setup/setup_pythonanywhere.sh
```

### **Step 4: Follow Web App Configuration**
(Same as Method 1, Steps 4-9)

---

## 🔐 **Security Configuration**

### **Generate New Secret Key**
```bash
cd /home/edumore360/EduMore360
source venv/bin/activate
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### **Update .env File**
```bash
nano .env
```

Replace `SECRET_KEY` with the generated key.

---

## 📊 **Wasabi S3 Setup**

### **Step 1: Create Wasabi Account**
1. Go to [wasabi.com](https://wasabi.com)
2. Create account and verify email

### **Step 2: Create Bucket**
1. Go to **"Buckets"** in Wasabi console
2. Click **"Create Bucket"**
3. Name: `edumore360-media`
4. Region: `us-east-1`
5. Make bucket **public**

### **Step 3: Get Access Keys**
1. Go to **"Access Keys"** in Wasabi
2. Click **"Create New Access Key"**
3. Copy **Access Key ID** and **Secret Access Key**

### **Step 4: Update Environment**
```env
WASABI_ACCESS_KEY_ID=your-access-key-id
WASABI_SECRET_ACCESS_KEY=your-secret-access-key
WASABI_STORAGE_BUCKET_NAME=edumore360-media
```

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
