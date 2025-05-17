#!/usr/bin/env python
"""
Monitoring script for EduMore360.
This script checks the health of various components and sends alerts if issues are detected.
"""

import os
import sys
import time
import requests
import smtplib
import psutil
import psycopg2
import redis
from email.mime.text import MIMEText
from datetime import datetime

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
import environ
env = environ.Env()
environ.Env.read_env(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env.production'))

# Configuration
SITE_URL = f"https://{env('ALLOWED_HOSTS').split(',')[0]}"
ADMIN_EMAIL = env('ADMIN_EMAIL', default='admin@example.com')
CHECK_INTERVAL = 300  # 5 minutes
ALERT_THRESHOLD = 3  # Number of consecutive failures before alerting

# Database connection
DB_URL = env('DATABASE_URL')
DB_USER = DB_URL.split('://')[1].split(':')[0]
DB_PASS = DB_URL.split('://')[1].split(':')[1].split('@')[0]
DB_HOST = DB_URL.split('@')[1].split(':')[0]
DB_PORT = DB_URL.split('@')[1].split(':')[1].split('/')[0]
DB_NAME = DB_URL.split('/')[-1]

# Redis connection
REDIS_URL = env('REDIS_URL')

# Email settings
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS')

# State tracking
failure_counts = {
    'website': 0,
    'database': 0,
    'redis': 0,
    'disk_space': 0,
    'memory': 0,
    'cpu': 0
}


def send_alert(subject, message):
    """Send an email alert."""
    try:
        msg = MIMEText(message)
        msg['Subject'] = f"EduMore360 Alert: {subject}"
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = ADMIN_EMAIL

        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        if EMAIL_USE_TLS:
            server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Alert sent: {subject}")
    except Exception as e:
        print(f"Failed to send alert: {e}")


def check_website():
    """Check if the website is responding."""
    try:
        response = requests.get(SITE_URL, timeout=10)
        if response.status_code == 200:
            failure_counts['website'] = 0
            return True
        else:
            failure_counts['website'] += 1
            if failure_counts['website'] >= ALERT_THRESHOLD:
                send_alert(
                    "Website Down",
                    f"The website at {SITE_URL} is returning status code {response.status_code}."
                )
            return False
    except Exception as e:
        failure_counts['website'] += 1
        if failure_counts['website'] >= ALERT_THRESHOLD:
            send_alert(
                "Website Unreachable",
                f"Failed to connect to {SITE_URL}: {str(e)}"
            )
        return False


def check_database():
    """Check if the database is responding."""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        failure_counts['database'] = 0
        return True
    except Exception as e:
        failure_counts['database'] += 1
        if failure_counts['database'] >= ALERT_THRESHOLD:
            send_alert(
                "Database Connection Failed",
                f"Failed to connect to database: {str(e)}"
            )
        return False


def check_redis():
    """Check if Redis is responding."""
    try:
        r = redis.from_url(REDIS_URL)
        r.ping()
        failure_counts['redis'] = 0
        return True
    except Exception as e:
        failure_counts['redis'] += 1
        if failure_counts['redis'] >= ALERT_THRESHOLD:
            send_alert(
                "Redis Connection Failed",
                f"Failed to connect to Redis: {str(e)}"
            )
        return False


def check_disk_space():
    """Check if disk space is sufficient."""
    try:
        disk = psutil.disk_usage('/')
        percent_free = 100 - disk.percent
        if percent_free < 10:  # Less than 10% free space
            failure_counts['disk_space'] += 1
            if failure_counts['disk_space'] >= ALERT_THRESHOLD:
                send_alert(
                    "Low Disk Space",
                    f"Server disk space is low: {percent_free:.1f}% free."
                )
            return False
        else:
            failure_counts['disk_space'] = 0
            return True
    except Exception as e:
        failure_counts['disk_space'] += 1
        if failure_counts['disk_space'] >= ALERT_THRESHOLD:
            send_alert(
                "Disk Space Check Failed",
                f"Failed to check disk space: {str(e)}"
            )
        return False


def check_memory():
    """Check if memory usage is within acceptable limits."""
    try:
        memory = psutil.virtual_memory()
        if memory.percent > 90:  # More than 90% used
            failure_counts['memory'] += 1
            if failure_counts['memory'] >= ALERT_THRESHOLD:
                send_alert(
                    "High Memory Usage",
                    f"Server memory usage is high: {memory.percent}% used."
                )
            return False
        else:
            failure_counts['memory'] = 0
            return True
    except Exception as e:
        failure_counts['memory'] += 1
        if failure_counts['memory'] >= ALERT_THRESHOLD:
            send_alert(
                "Memory Check Failed",
                f"Failed to check memory usage: {str(e)}"
            )
        return False


def check_cpu():
    """Check if CPU usage is within acceptable limits."""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        if cpu_percent > 90:  # More than 90% used
            failure_counts['cpu'] += 1
            if failure_counts['cpu'] >= ALERT_THRESHOLD:
                send_alert(
                    "High CPU Usage",
                    f"Server CPU usage is high: {cpu_percent}% used."
                )
            return False
        else:
            failure_counts['cpu'] = 0
            return True
    except Exception as e:
        failure_counts['cpu'] += 1
        if failure_counts['cpu'] >= ALERT_THRESHOLD:
            send_alert(
                "CPU Check Failed",
                f"Failed to check CPU usage: {str(e)}"
            )
        return False


def run_checks():
    """Run all health checks."""
    print(f"Running health checks at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    website_status = check_website()
    db_status = check_database()
    redis_status = check_redis()
    disk_status = check_disk_space()
    memory_status = check_memory()
    cpu_status = check_cpu()
    
    print(f"Website: {'OK' if website_status else 'FAIL'}")
    print(f"Database: {'OK' if db_status else 'FAIL'}")
    print(f"Redis: {'OK' if redis_status else 'FAIL'}")
    print(f"Disk Space: {'OK' if disk_status else 'FAIL'}")
    print(f"Memory: {'OK' if memory_status else 'FAIL'}")
    print(f"CPU: {'OK' if cpu_status else 'FAIL'}")
    print("-" * 40)


if __name__ == "__main__":
    print("Starting EduMore360 monitoring service...")
    
    while True:
        try:
            run_checks()
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("Monitoring service stopped.")
            break
        except Exception as e:
            print(f"Error in monitoring service: {e}")
            time.sleep(CHECK_INTERVAL)
