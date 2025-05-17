<<<<<<< HEAD
# EduMore360

EduMore360 is a comprehensive educational platform for students from kindergarten through grade 12, aligned with US and Ghana curriculum standards. The platform provides interactive learning experiences, quizzes with immediate feedback, and progress tracking.

## Features

- **Comprehensive Curriculum**: Access educational content organized by grade level, subject, and topic.
- **Interactive Quizzes**: Test your knowledge with timed quizzes and receive immediate feedback.
- **Progress Tracking**: Monitor your learning progress and achievements.
- **Mobile-First Design**: Responsive design for optimal experience on all devices.
- **Subscription Plans**: Free and premium subscription options for individuals, families, and enterprises.
- **User Management**: Family and enterprise subscription management with group features.

## Technology Stack

- **Backend**: Django 5.0
- **Frontend**: Tailwind CSS, DaisyUI, Alpine.js, HTMX
- **Database**: PostgreSQL (configurable)
- **Caching**: Redis
- **Task Queue**: Celery
- **Payment Processing**: Paystack

## Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL (optional, can use SQLite for development)
- Redis (optional, for caching and Celery)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/edumore360.git
   cd edumore360
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv

   # On Windows
   .\venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the variables in `.env` with your configuration

5. Run the setup script:
   ```
   python setup.py
   ```
   This will:
   - Run migrations
   - Create a superuser
   - Populate sample data
   - Set up Tailwind CSS
   - Collect static files

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Manual Setup (Alternative to setup.py)

If you prefer to set up the project manually:

1. Run migrations:
   ```
   python manage.py makemigrations accounts core curriculum quiz subscription
   python manage.py migrate
   ```

2. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

3. Populate sample data:
   ```
   python scripts/populate_sample_data.py
   ```

4. Set up Tailwind CSS:
   ```
   cd theme/static_src
   npm install
   npm run build
   cd ../..
   ```

5. Collect static files:
   ```
   python manage.py collectstatic
   ```

## Development

### Running Tests

```
python manage.py test
```

### Tailwind CSS Development

For Tailwind CSS development with hot reloading:

```
cd theme/static_src
npm run dev
```

### Celery Workers

To run Celery workers for background tasks:

```
celery -A edumore360 worker -l info
```

## Production Deployment

EduMore360 is designed to be deployed in a production environment using Render, traditional server deployment, or Docker containers.

### Option 1: Render Deployment (Recommended)

This project includes configuration files for easy deployment on Render.

1. Fork or clone this repository to your GitHub account.

2. In the Render dashboard, click "New" and select "Blueprint".

3. Connect your GitHub repository.

4. Render will automatically detect the `render.yaml` file and set up the services:
   - Web service (Django application)
   - Worker service (Celery)
   - PostgreSQL database

5. Add the required environment variables that are marked as `sync: false` in the render.yaml file:
   - `EMAIL_HOST_USER`: Your email address
   - `EMAIL_HOST_PASSWORD`: Your email app password
   - `DEFAULT_FROM_EMAIL`: Your email address
   - `PAYSTACK_SECRET_KEY`: Your Paystack secret key
   - `PAYSTACK_PUBLIC_KEY`: Your Paystack public key

6. Deploy the application.

#### Manual Render Setup (Alternative to Blueprint)

If you prefer to set up the services manually:

1. Create a PostgreSQL database on Render.

2. Create a Web Service:
   - Connect your GitHub repository
   - Select the branch to deploy
   - Use "Python" as the environment
   - Set the build command to `./build.sh`
   - Set the start command to `gunicorn edumore360.wsgi:application`

3. Add the following environment variables:
   - `DEBUG`: false
   - `SECRET_KEY`: (generate a secure key)
   - `ALLOWED_HOSTS`: your-app.onrender.com
   - `DATABASE_URL`: (your PostgreSQL connection string)
   - `EMAIL_HOST`: smtp.gmail.com
   - `EMAIL_PORT`: 587
   - `EMAIL_USE_TLS`: true
   - `EMAIL_HOST_USER`: (your email)
   - `EMAIL_HOST_PASSWORD`: (your app password)
   - `DEFAULT_FROM_EMAIL`: (your email)
   - `PAYSTACK_SECRET_KEY`: (your Paystack secret key)
   - `PAYSTACK_PUBLIC_KEY`: (your Paystack public key)

4. Create a Background Worker for Celery:
   - Connect to the same repository
   - Set the build command to `./build.sh`
   - Set the start command to `celery -A edumore360 worker --loglevel=info`
   - Use the same environment variables as the web service

### Option 2: Traditional Server Deployment

1. Set up a production server (Ubuntu 22.04 LTS recommended)

2. Clone the repository and install dependencies:
   ```bash
   git clone https://github.com/yourusername/edumore360.git
   cd edumore360
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Configure production environment:
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

4. Set up the database (PostgreSQL recommended):
   ```bash
   sudo -u postgres createuser -P edumore360
   sudo -u postgres createdb -O edumore360 edumore360
   ```

5. Apply migrations and collect static files:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

6. Set up Gunicorn as a systemd service:
   ```bash
   sudo cp scripts/systemd/gunicorn-edumore360.service /etc/systemd/system/
   # Edit the service file to match your paths
   sudo systemctl enable gunicorn-edumore360
   sudo systemctl start gunicorn-edumore360
   ```

7. Set up Celery workers:
   ```bash
   sudo cp scripts/systemd/celery-edumore360.service /etc/systemd/system/
   # Edit the service files to match your paths
   sudo systemctl enable celery-edumore360
   sudo systemctl start celery-edumore360
   ```

8. Configure Nginx:
   ```bash
   sudo cp nginx/conf.d/edumore360.conf /etc/nginx/sites-available/edumore360
   # Edit the configuration file to match your domain
   sudo ln -s /etc/nginx/sites-available/edumore360 /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Option 3: Docker Deployment

1. Configure production environment:
   ```bash
   cp .env.example .env
   # Edit .env with your production settings
   ```

2. Build and start Docker containers:
   ```bash
   docker-compose up -d
   ```

3. Apply migrations:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### Production Checklist

Before going live, make sure to:

1. Set `DEBUG=False` in your production environment
2. Use strong, unique passwords for all services
3. Configure proper SSL/TLS for secure connections
4. Set up regular database backups using `scripts/backup.sh`
5. Configure monitoring using `scripts/monitor.py`
6. Review the full production checklist in `docs/production_checklist.md`

### Scaling Considerations

For high-traffic deployments:

1. Use a load balancer to distribute traffic across multiple web servers
2. Scale Celery workers horizontally for background task processing
3. Consider database read replicas for read-heavy workloads
4. Use a CDN for static file delivery
5. Implement caching strategies for frequently accessed data

## Project Structure

- `accounts/`: User authentication and profile management
- `core/`: Core functionality and shared components
- `curriculum/`: Curriculum, subjects, topics, and educational content
- `quiz/`: Quiz engine and question management
- `subscription/`: Subscription plans and payment processing
- `theme/`: Tailwind CSS configuration and styles
- `templates/`: HTML templates
- `static/`: Static files (CSS, JavaScript, images)
- `media/`: User-uploaded files
- `scripts/`: Utility scripts

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For questions or support, please contact [your-email@example.com](mailto:your-email@example.com).
=======
# edumore360
>>>>>>> 95d489ad35498b578cce8f23739e66b6d614803f
