# EduMore360 Production Deployment Checklist

This document provides a comprehensive checklist for deploying EduMore360 to a production environment.

## Pre-Deployment Checks

- [ ] Run all tests to ensure they pass
  ```bash
  python manage.py test
  ```
- [ ] Check for security vulnerabilities in dependencies
  ```bash
  pip install safety
  safety check -r requirements.txt
  ```
- [ ] Ensure all environment variables are set in `.env.production`
- [ ] Verify database backups are configured
- [ ] Check that all static files are collected
  ```bash
  python manage.py collectstatic --noinput
  ```
- [ ] Verify that all migrations are applied
  ```bash
  python manage.py migrate
  ```

## Server Setup

- [ ] Set up a production-ready server (Ubuntu 22.04 LTS recommended)
- [ ] Install required system packages
  ```bash
  sudo apt update
  sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx redis-server supervisor
  ```
- [ ] Set up a PostgreSQL database
  ```bash
  sudo -u postgres createuser -P edumore360
  sudo -u postgres createdb -O edumore360 edumore360
  ```
- [ ] Configure Redis for caching and Celery
- [ ] Set up a virtual environment
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## SSL/TLS Configuration

- [ ] Obtain SSL certificates (Let's Encrypt recommended)
  ```bash
  sudo apt install certbot python3-certbot-nginx
  sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
  ```
- [ ] Configure Nginx with SSL
- [ ] Set up auto-renewal for SSL certificates
  ```bash
  sudo certbot renew --dry-run
  ```

## Application Deployment

- [ ] Clone the repository
  ```bash
  git clone https://github.com/yourusername/edumore360.git
  cd edumore360
  ```
- [ ] Create and configure `.env.production` file
- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```
- [ ] Run migrations
  ```bash
  python manage.py migrate
  ```
- [ ] Collect static files
  ```bash
  python manage.py collectstatic --noinput
  ```
- [ ] Set up Gunicorn
  ```bash
  sudo cp scripts/systemd/gunicorn-edumore360.service /etc/systemd/system/
  sudo systemctl enable gunicorn-edumore360
  sudo systemctl start gunicorn-edumore360
  ```
- [ ] Set up Celery
  ```bash
  sudo cp scripts/systemd/celery-edumore360.service /etc/systemd/system/
  sudo cp scripts/systemd/celerybeat-edumore360.service /etc/systemd/system/
  sudo systemctl enable celery-edumore360 celerybeat-edumore360
  sudo systemctl start celery-edumore360 celerybeat-edumore360
  ```
- [ ] Configure Nginx
  ```bash
  sudo cp nginx/conf.d/edumore360.conf /etc/nginx/sites-available/edumore360
  sudo ln -s /etc/nginx/sites-available/edumore360 /etc/nginx/sites-enabled/
  sudo nginx -t
  sudo systemctl reload nginx
  ```

## Docker Deployment (Alternative)

- [ ] Install Docker and Docker Compose
  ```bash
  sudo apt install docker.io docker-compose
  ```
- [ ] Configure `.env.production` file
- [ ] Build and start Docker containers
  ```bash
  docker-compose up -d
  ```

## Post-Deployment Checks

- [ ] Verify the application is running
  ```bash
  curl -I https://yourdomain.com
  ```
- [ ] Check for any errors in logs
  ```bash
  sudo journalctl -u gunicorn-edumore360
  sudo journalctl -u celery-edumore360
  sudo journalctl -u celerybeat-edumore360
  ```
- [ ] Test all critical functionality
  - [ ] User registration and login
  - [ ] Content access
  - [ ] Payment processing
  - [ ] Quiz functionality
- [ ] Set up monitoring
  - [ ] Configure Sentry for error tracking
  - [ ] Set up server monitoring (e.g., Prometheus, Grafana)
  - [ ] Configure log rotation

## Security Checks

- [ ] Run security scan
  ```bash
  python manage.py check --deploy
  ```
- [ ] Verify firewall settings
  ```bash
  sudo ufw status
  ```
- [ ] Check SSL/TLS configuration
  ```bash
  curl https://www.ssllabs.com/ssltest/analyze.html?d=yourdomain.com
  ```
- [ ] Ensure sensitive data is not exposed
- [ ] Verify backup procedures are working

## Maintenance Procedures

- [ ] Set up regular database backups
  ```bash
  # Add to crontab
  0 2 * * * pg_dump -U edumore360 edumore360 | gzip > /path/to/backups/edumore360_$(date +\%Y\%m\%d).sql.gz
  ```
- [ ] Configure log rotation
  ```bash
  sudo nano /etc/logrotate.d/edumore360
  ```
- [ ] Document deployment process
- [ ] Create rollback procedures
- [ ] Set up monitoring alerts

## Performance Optimization

- [ ] Enable caching
- [ ] Configure CDN for static files
- [ ] Optimize database queries
- [ ] Set up database connection pooling
- [ ] Configure proper worker settings for Gunicorn and Celery

## Scaling Considerations

- [ ] Identify potential bottlenecks
- [ ] Plan for horizontal scaling
- [ ] Consider load balancing options
- [ ] Evaluate database scaling options
