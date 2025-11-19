# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django REST API backend for a job application tracker. The API serves a frontend application (deployed at cs-job-tracker.web.app) and provides endpoints for managing job applications with statuses (wishlist, applied, interviewing, offer).

**Tech Stack:**
- Django 5.1.3 with Django REST Framework 3.15.2
- Python 3.13
- Token-based authentication
- SQLite database
- Gunicorn 23.0.0 for production deployment
- WhiteNoise 6.8.2 for static files
- CORS headers configured for frontend (localhost:3000 and Firebase hosting)

## Development Commands

### Initial Setup
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create/apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin access)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic
```

### Running the Application
```bash
# Development server (default: http://127.0.0.1:8000)
python manage.py runserver

# Run on specific port
python manage.py runserver 8080
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations tracker

# Apply migrations
python manage.py migrate

# Open Django shell for debugging
python manage.py shell
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test tracker

# Run specific test class
python manage.py test tracker.tests.TestClassName
```

## Architecture

### Project Structure
- **mysite/**: Django project configuration
  - `settings.py`: Main configuration (auth, CORS, static files, REST framework)
  - `urls.py`: Root URL routing (admin + tracker app)
- **tracker/**: Main application (all business logic)
  - `models.py`: Data models (Account, Job, Contact)
  - `views.py`: API endpoints (all function-based views)
  - `serializers.py`: DRF serializers for data validation
  - `urls.py`: App-level URL routing

### Data Models

**Account** (Custom User Model)
- Extends AbstractBaseUser with custom fields
- Uses username as USERNAME_FIELD
- Additional fields: first_name, last_name, is_pro, about, night_mode, github, linkedin, website, is_public, image, last_lesson_url
- Custom manager: MyAccountManager (handles user creation)

**Job**
- Belongs to Account (ForeignKey)
- Status choices: wishlist, applied, interviewing, offer
- Has rank field for ordering within status columns
- Includes to_dict() method for serialization to frontend format (camelCase)

**Contact**
- Belongs to Job (ForeignKey)
- Stores contact information for people related to job applications

### Authentication

Uses Django REST Framework Token Authentication:
- Tokens auto-created via post_save signal in serializers.py:32-34
- Login endpoint: `/api/login/` (obtain_auth_token)
- Register endpoint: `/api/register/` (returns token on successful registration)
- Protected views use `@permission_classes((IsAuthenticated,))`
- Token must be sent in Authorization header: `Token <token_value>`

### API Endpoints

All routes defined in tracker/urls.py:
- GET `/jobs/` - Get all jobs for authenticated user, grouped by status
- GET `/jobs/<job_id>/` - Get single job
- POST `/jobs/add/` - Create new job
- POST `/jobs/update/<job_id>/` - Update job fields
- POST `/jobs/update/` - Bulk update jobs (for drag-and-drop reordering)
- POST `/jobs/description/update/<job_id>/` - Update job description only
- POST `/jobs/notes/update/<job_id>/` - Update job notes only
- GET `/jobs/contacts/get/<job_id>/` - Get contacts for a job
- POST `/jobs/contacts/add/<job_id>/` - Add contact to a job
- POST `/jobs/contacts/update/<contact_id>/` - Update contact

### Key Implementation Details

**Job Reordering (views.py:37-53)**
- The `/jobs/update/` endpoint handles drag-and-drop reordering
- Frontend sends updated columnMap with jobs grouped by status
- Backend calculates position changes and updates status + rank fields
- Only fetches jobs from affected columns for efficiency

**User Ownership Validation**
- All job/contact operations validate that job.user == request.user
- Prevents users from accessing/modifying other users' data

**Environment Configuration**
- Uses python-dotenv for environment variables
- SECRET_KEY loaded from .env file with fallback value
- DEBUG is False by default (production-ready)
- ALLOWED_HOSTS configured for Heroku deployment

## Notes for Development

- Settings module: `mysite.settings` (configured in manage.py)
- Custom user model defined via `AUTH_USER_MODEL = 'tracker.Account'` in settings.py:147
- All views are function-based (using @api_view decorator)
- Frontend expects camelCase keys - Job.to_dict() handles conversion
- The rank field on Job model is stored as CharField (not IntegerField)

## Deployment (Render.com)

### Python Version
This project uses **Python 3.13** via `.python-version` file.

All dependencies are compatible with Python 3.13. The project does not use PostgreSQL, SQLAlchemy, or greenlet, so it avoids the Python 3.13 compatibility issues that affect those libraries.

### Deployment Configuration

**Build Command**: `./build.sh`
- The build script handles: dependency installation, static file collection, and database migrations
- Build script is located at project root: `build.sh`

**Start Command**: `gunicorn mysite.wsgi --log-file -`
- Defined in `Procfile` for compatibility with Heroku/Render

### Environment Variables (Required for Production)

Set these in your Render.com dashboard:

```bash
# Django settings
SECRET_KEY=<your-secret-key-here>  # Generate a strong secret key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,yourdomain.com

# Database (if using PostgreSQL on Render)
DATABASE_URL=<provided-by-render-postgresql>
```

### Pre-deployment Checklist

1. Set all required environment variables in Render dashboard
2. Configure build command: `./build.sh`
3. Configure start command: `gunicorn mysite.wsgi --log-file -`
4. SQLite database will be used (stored in `/opt/render/project/src/db.sqlite3` on Render)
5. Note: SQLite data will be lost on redeploys - for persistent data, consider upgrading to PostgreSQL

### Static Files

Static files are handled by WhiteNoise (configured in settings.py):
- Middleware order is optimized (WhiteNoise after SecurityMiddleware)
- `STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')`
- Files collected during build via `python manage.py collectstatic --no-input`

### Database Considerations

Currently configured for SQLite (development). For production on Render:
- Use Render's PostgreSQL database
- Install `psycopg2-binary`
- Update settings.py to parse DATABASE_URL environment variable
- Example: `dj-database-url` package can help parse DATABASE_URL
