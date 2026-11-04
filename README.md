# eartech-internship-2026
EarTech internship projects: CourseHub (Team A) and HealthPulse (Team B)

# CourseHub

CourseHub is a collaborative learning management
platform built with Django.

## Project Overview

The platform is designed to support:

- User account management
- Course management
- Student enrollments
- Course reviews and ratings

## Technology Stack

- Python 3.12
- Django 5.2 LTS
- SQLite (development database)
- Git
- Azure DevOps

## Development Setup

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd coursehub
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment (Windows)

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Run database migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Project Structure

- coursehub/: Django project configuration
- accounts/: User account management
- courses/: Course management
- enrollments/: Enrollment management
- reviews/: Course reviews

## Team Workflow

- main: Stable shared branch
- feature/*: Individual development branches
- All changes must be submitted through Pull Requests.
- Direct commits to main are not allowed.
