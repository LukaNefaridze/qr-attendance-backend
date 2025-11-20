QR Attendance System - Project Context
Project Overview

Name: QR Attendance System
Description: Digital attendance ecosystem for universities with QR-based check-in system
Tech Stack:

Frontend: React (Web Panel for Professors/Admin)
Mobile: Flutter (Student App)
Backend: Django REST Framework
Database: MySQL
Auth: JWT
Security: HMAC-signed QR codes



Architecture Overview
System Components

Flutter Mobile App (Students)

Authorization
QR Scanner
Attendance recording
Attendance history
Profile management


React Web Panel (Professors & Admin)

Professor: Today's lectures → Start Session → Generate QR
Professor: Live attendance monitoring
Admin: Users, Courses, Schedule, Enrollment management
Admin: System statistics and export


Django REST Backend API

CRUD operations for all models
HMAC QR code generation
Session logic (Start Session only - no manual stop)
Attendance scan validation
Export endpoints


MySQL Database

Users, Courses, Enrollment
Timetable, Sessions, Attendance



Code Conventions
Naming

Files: snake_case (e.g., models.py, views.py, serializers.py)
Variables: snake_case (e.g., user_profile, course_code, attendance_record)
Constants: UPPER_SNAKE_CASE (e.g., DAYS_OF_WEEK, MAX_QR_EXPIRY_MINUTES)
Classes: PascalCase (e.g., User, Course, Attendance, Session)
URLs: kebab-case (e.g., /api/start-session, /api/attendance-history)

Style Guidelines

Indentation: 4 spaces (PEP 8)
Quotes: Single quotes for strings (Django convention)
Line length: 79-88 characters (PEP 8)
Imports: Grouped (stdlib, third-party, local) with blank lines

Patterns to Follow

API Views: Django REST Framework ViewSets (ModelViewSet, ReadOnlyViewSet)
Error handling: DRF exception handlers with proper status codes
Serializers: ModelSerializer for CRUD, nested serializers for relationships
Authentication: JWT tokens via PyJWT
QR Security: HMAC-signed QR codes with expiration timestamps
Testing: Django TestCase with DRF APIClient

Dependencies & Tools

Package Manager: pip
Requirements: requirements.txt (Django>=5.2.7, djangorestframework>=3.14.0)
Database: MySQL (mysqlclient>=2.2.0)
Authentication: PyJWT>=2.8.0
Security: cryptography>=41.0.0 (for HMAC QR signing)
Linter: flake8, pylint (optional)
Formatter: black (optional)

Key Files & Directories
/core
  models.py       - User, Course, Enrollment, Timetable, Session, Attendance models
  views.py        - API ViewSets (UserViewSet, CourseViewSet, etc.)
  serializers.py  - DRF serializers for all models
  admin.py        - Django admin configuration
/attendance_system
  settings.py     - Django project settings (database, installed apps, etc.)
  urls.py         - Main URL routing with DRF router
  wsgi.py         - WSGI configuration
  asgi.py         - ASGI configuration
/migrations       - Django database migrations
requirements.txt  - Python package dependencies
manage.py         - Django management script

Development Workflow

Start dev server: python manage.py runserver
Run migrations: python manage.py makemigrations && python manage.py migrate
Create superuser: python manage.py createsuperuser
Run tests: python manage.py test
Database setup: Run setup_database.bat (Windows) or equivalent script
Branch naming: feature/description, bugfix/description, hotfix/description

Important Notes

Security: QR codes are HMAC-signed with expiration timestamps to prevent replay attacks
Sessions: Once started, sessions remain active until expiration (no manual stop)
Attendance: Unique constraint on (student, session) prevents duplicate scans
User roles: is_student and is_professor flags on User model (extends AbstractUser)
Database: MySQL configured via settings.py (see DJANGO_MYSQL_SYNC.md)
IP tracking: Optional IP address logging in Attendance model for security auditing
Related names: Custom related_name on User.groups and User.user_permissions to avoid clashes

Current Focus

Database synchronization between Django and MySQL
Flutter mobile app integration (see FLUTTER_INTEGRATION_ANALYSIS.md)
QR code generation and validation endpoints
Session management and attendance tracking
Admin panel configuration for course and user management

Preferences

Use Django REST Framework ViewSets for consistent API structure
Follow Django best practices and PEP 8 for Python code
Prefer explicit over implicit (clear model relationships, verbose field names)
Document complex logic (QR signing, session expiration) with comments
Use Django's built-in features (Model Meta options, validators) before custom solutions
